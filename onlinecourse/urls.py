from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path(route='', view=views.CourseListView.as_view(), name='index'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('registration/', views.registration_request, name='registration'),
    # ex: /onlinecourse/5/
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    # ex: /enroll/5/
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name = 'exam_result'),
    # <HINT> Create a route for submit view

    # <HINT> Create a route for show_exam_result view

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
