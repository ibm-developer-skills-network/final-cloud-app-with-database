from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Course, Enrollment, Submission, Choice, Submission, Lesson
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging

logger = logging.getLogger(__name__)


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
        num_results = Enrollment.objects.filter(
            user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


class CourseListView(generic.ListView):

    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
                logger.info("User: %s, Course: %s", user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'
    logger.info("model: %s", model)


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


def submit(request, course_id):
    if request.method == "POST":
        context = {}
        user = request.user
        course = get_object_or_404(Course, pk=course_id)
        enrollment = get_object_or_404(Enrollment, user=user, course=course)
        submission = Submission.objects.create(enrollment=enrollment)

        def extract_answers_ids(request):
            submitted_answers = []
            for key in request.POST:
                if key.startswith('choice'):
                    value = request.POST[key]
                    choice_id = int(value)
                    submitted_answers.append(choice_id)
            return submitted_answers

        answer_ids = extract_answers_ids(request)

        def extract_answers(request):
            submitted_answers = []
            for key in request.POST:
                if key.startswith('choice_text'):
                    value = request.POST[key]
                    choice_id = int(value)
                    submitted_answers.append(choice_id)
            return submitted_answers

        answers = extract_answers(request)

        for answer_id in answer_ids:
            choice = get_object_or_404(
                Choice, pk=answer_id)
            submission.choices.add(choice)

        submission.save()

        context = {
            'submission_id': submission.id,
            'submission': submission,
            'choices': submission.choices,
            'answer_ids': answer_ids,
            'answers': answers,
        }
        return render(request, 'onlinecourse/exam_result_bootstrap.html', context)


def retake_exam(request, course_id):
    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course_id,)))


class ExamResults(generic.DetailView):
    model = Submission
    template_name = 'results'


def show_exam_result(request, course_id):
    context = {}
    submission_id = request.POST['submission_id']
    answer_ids = request.answer_ids
    courses = Course.objects.order_by('-total_enrollment')[:10]
    course = get_object_or_404(Course, pk=course_id)
    lesson = get_object_or_404(Lesson, pk=course_id)
    score = submission.calculate_score()
    submission = Submission.objects.get(pk=submission_id)

    context = {
        'course': course,
        'courses': courses,
        'submission': submission,
        'submission_id': submission_id,
        'choices': submission.choices,
        'answer_ids': answer_ids,
        'score': score,
        'lesson': lesson,
    }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
