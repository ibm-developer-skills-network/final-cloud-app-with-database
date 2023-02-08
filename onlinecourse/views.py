from django.shortcuts import render
from django.http import HttpResponseRedirect
# <HINT> Import any new Models here
from .models import Course, Enrollment, Question, Choice, Submission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


# CourseListView
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


# A method to collect the selected choices from the exam form from the request object
def extract_answers(request):
   submitted_answers = []
   for key in request.POST:
       if key.startswith('choice'):
           value = request.POST[key]
           choice_id = int(value)
           submitted_answers.append(choice_id)
   return submitted_answers


def submit(request, course_id):
    # Getting the current user, course object and the user's enrollment
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    enrollment = Enrollment.objects.get(user=user, course=course)

    # Creating a new Submission object / Submission table entry in db
    submission = Submission.objects.create(enrollment=enrollment)

    # Extracting the selected choices from the POST request
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_answers.append(choice_id)

    # Adding the selected choices to the Submission table (model)
    for choice_id in submitted_answers:
        choice_obj = Choice.objects.get(id=choice_id)
        submission.choices.add(choice_obj)
    submission.save()  # saving the changes
    print(f"Submitted exam for user {user} in course {course_id}")

    # Redirecting to the show_exam_result view with the submission id
    return HttpResponseRedirect(reverse(viewname='onlinecourse:show_exam_result', args=(course_id, submission.id)))


def show_exam_result(request, course_id, submission_id):
    course_obj = Course.objects.get(id=course_id)

    context = {}
    context['course'] = course_obj

    submission_choices = Submission.objects.get(id=submission_id).choices.all()
    context['choices'] = submission_choices
    print("Submission choices: \n", submission_choices)

    all_exam_questions = Question.objects.filter(courses=course_id)
    context['questions'] = all_exam_questions
    print("All exam questions: \n", all_exam_questions)

    all_exam_choices = [question.choice_set for question in all_exam_questions]
    print("All exam choices: \n", all_exam_choices)

    # Calculate the submission score
    submission_score = 0
    max_score = 0
    for question in all_exam_questions:
        max_score += question.marks
        if question.answered_correctly(submission_choices):
            submission_score += question.marks
        
    # Determine a grade (points are % correct, rounded to nearest whole integer)
    context['grade'] = round(submission_score / max_score * 100)
    print("Submission grade: ", submission_score)

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)