from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "onlinecourse"
urlpatterns = [
 
    path(route="", view=views.CourseListView.as_view(), name="index"),
    path("registration/", views.registration_request, name="registration"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    
    # question path
    path("<int:course_id>/", views.combined_course_detail, name="course_and_question_detail"),
    # course details path
    path("<int:pk>/", views.CourseDetailView.as_view(), name="course_details"),
    # enroll path
    path("<int:course_id>/enroll/", views.enroll, name="enroll"),
    # submit path
    path("<int:course_id>/submit/", views.submit_view, name="submit"),
    # exam result path
    path(
        "course/<int:course_id>/submission/<int:submission_id>/result/",
        views.show_exam_result,
        name="show_exam_result",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
