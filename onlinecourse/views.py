from typing import Any
from django.db import models
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Course, Enrollment, Question, Choice, Submission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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


# CourseDetailView
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = "onlinecourse/course_detail_bootstrap.html"


# Combined course and question detail view
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


# Enroll view
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


# Submit view
def submit_view(request, course_id):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=user, course=course)

    if request.method == "POST":
        submission = Submission.objects.create(enrollment=enrollment)
        submission.save()

        selected_choices = extract_answers(request)

        for choice_id in selected_choices:
            submission.choices.add(choice_id)

    return HttpResponseRedirect(
        reverse(
            viewname="onlinecourse:show_exam_result",
            args=(
                course.id,
                submission.id,
            ),
        )
    )


# Extract answers from request
def extract_answers(request):
    submitted_anwsers = []
    for key in request.POST:
        if key.startswith("choice"):
            value = request.POST[key]
            choice_id = int(value)
            submitted_anwsers.append(choice_id)
    return submitted_anwsers


# Show exam result view
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    questioners = Question.objects.filter(course=course_id)
    choices = submission.choices.all()

    
    selected_choice_ids = (
        submission.choices.all()
        .filter(question__course=course)
        .values_list("id", flat=True)
    )

    total_score = 0
    question_results = []

    for choice_id in selected_choice_ids:
        choice = get_object_or_404(Choice, pk=choice_id)
        question = Question.objects.get(pk=choice.question_id)

        is_correct = choice.is_correct

        if is_correct:
            total_score += question.grade
            print(total_score)

        question_results.append(
            {
                "question_text": question.question_text,
                "selected_choice": choice.choice_text,
                "is_correct": is_correct,
            }
        )

    print(question_results)

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
