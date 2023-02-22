from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib import admin

app_name = 'onlinecourse'
urlpatterns = [
    path('', views.CourseListView.as_view(), name='index'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    path('<int:pk>/', views.retake_exam, name='retake_exam'),
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('<int:course_id>/submit/results',
         views.show_exam_result, name='results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
