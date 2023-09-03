from typing import Any
from django.db import models
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


# def question_detail(request, question_id):
#     question = Question.objects.get(pk=question_id)
#     context = {
#         'question': question,
#         'question_id': question_id,
#     }
#     return render(request, 'onlinecourse/course_detail_bootstrap.html', context)


# def question_detail(request, course_id):
#     question = Question.objects.get(pk=course_id)
#     context = {
#         'question': question,
#         'course_id': course_id,
#     }
#     return render(request, 'onlinecourse/course_detail_bootstrap.html', context)


def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "onlinecourse/user_registration_bootstrap.html", context)
    elif request.method == "POST":
        # Check if user exists
        username = request.POST["username"]
        password = request.POST["psw"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context["message"] = "User already exists."
            return render(
                request, "onlinecourse/user_registration_bootstrap.html", context
            )


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context["message"] = "Invalid username or password."
            return render(request, "onlinecourse/user_login_bootstrap.html", context)
    else:
        return render(request, "onlinecourse/user_login_bootstrap.html", context)


def logout_request(request):
    logout(request)
    return redirect("onlinecourse:index")


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
    template_name = "onlinecourse/course_list_bootstrap.html"
    context_object_name = "course_list"

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by("-total_enrollment")[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = "onlinecourse/course_detail_bootstrap.html"


def combined_course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    question = Question.objects.filter(course=course_id)
    choice = Choice.objects.order_by("-question_id")[:20]

    context = {
        "course": course,
        "question": question,
        "choice": choice,
    }

    return render(request, "onlinecourse/course_detail_bootstrap.html", context)


# class QuestionListView(generic.ListView):
#     template_name = 'onlinecourse/course_detail_bootstrap.html'
#     context_object_name = 'question_list'

#     def get_queryset(self):
#         question = Question.objects.order_by('-grade')[:10]
#         return question


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode="honor")
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(
        reverse(viewname="onlinecourse:course_details", args=(course.id,))
    )


# <HINT> Create a submit view to create an exam submission record for a course enrollment,
# you may implement it based on following logic:
# Get user and course object, then get the associated enrollment object created when the user enrolled the course
# Create a submission object referring to the enrollment
# Collect the selected choices from exam form
# Add each selected choice object to the submission object
# Redirect to show_exam_result with the submission id


def submit_view(request, course_id):
    # Get the current user and the course object, then get the associated the enrollment object
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=user, course=course)

    if request.method == "POST":
        # Create a submission object referring to the enrollment
        submission = Submission.objects.create(enrollment=enrollment)
        submission.save()

        # Collect the selected choices from HTTP request object
        selected_choices = extract_answers(request)

        # Add each selected choice object to the submission object
        for choice_id in selected_choices:
            submission.choices.add(choice_id)

        # Redirect to a show_exam_result view with the submission id to show the exam result
        # return redirect("show_exam_result/" + f"{submission.id}")

    return HttpResponseRedirect(
        reverse(
            viewname="onlinecourse:show_exam_result",
            args=(
                course.id,
                submission.id,
            ),
        )
    )

    # # Render the exam submission form
    # choices = Choice.objects.filter(question__course=course)
    # return render(
    #     request, "onlinecourse/exam_result_bootstrap.html", {"choices": choices}
    # )


# <HINT> A example method to collect the selected choices from the exam form from the request object
def extract_answers(request):
    submitted_anwsers = []
    for key in request.POST:
        if key.startswith("choice"):
            value = request.POST[key]
            choice_id = int(value)
            submitted_anwsers.append(choice_id)
    return submitted_anwsers


# <HINT> Create an exam result view to check if learner passed exam and show their question results and result for each question,
# you may implement it based on the following logic:
# Get course and submission based on their ids
# Get the selected choice ids from the submission record
# For each selected choice, check if it is a correct answer or not
# Calculate the total score
def show_exam_result(request, course_id, submission_id):
    # Get the course object and submission object based on their ids in view arguments
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    questioners = Question.objects.filter(course=course_id)
    choices = submission.choices.all()

    # Get the selected choice ids from the submission record
    # selected_choice_ids = submission.choices.filter(question__course=course).values_list("id", flat=True)

    selected_choice_ids = (
        submission.choices.all()
        .filter(question__course=course)
        .values_list("id", flat=True)
    )

    total_score = 0
    question_results = []

    # For each selected choice, check if it is a correct answer or not
    for choice_id in selected_choice_ids:
        choice = get_object_or_404(Choice, pk=choice_id)
        question = Question.objects.get(pk=choice.question_id)

        # Check if the selected choice is correct
        is_correct = choice.is_correct

        # Calculate the total score by adding up the grades for all questions in the course
        if is_correct:
            total_score += question.grade
            print(total_score)

        # Append the result for each question
        question_results.append(
            {
                "question_text": question.question_text,
                "selected_choice": choice.choice_text,
                "is_correct": is_correct,
            }
        )

    print(question_results)

    # Add the course, selected_ids, and grade to context for rendering HTML page
    context = {
        "course": course,
        "submission": submission,
        "total_score": total_score,
        "selected_choice_ids": selected_choice_ids,
        "question_results": question_results,
        "questioners": questioners,
        "choices": choices,
    }

    return render(request, "onlinecourse/exam_result_bootstrap.html", context)
