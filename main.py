# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Your application specific imports
from data.models import *
from datetime import date


def clean_data():
    # Delete all
    User.objects.all().delete()
    Learner.objects.all().delete()
    Instructor.objects.all().delete()
    Course.objects.all().delete()
    Enrollment.objects.all().delete()


def populate_database():
    # Add user
    user = User(first_name='John', last_name='Doe', dob=date(1962, 7, 16))
    user.save()
    # Add Learners
    learner_james = Learner(first_name='James', last_name='Smith', dob=date(1962, 7, 16),
                            occupation='data_scientist',
                            social_link='https://www.linkedin.com/james/')
    learner_james.save()
    learner_mary = Learner(first_name='Mary', last_name='Smith', dob=date(1991, 6, 12), occupation='dba',
                           social_link='https://www.facebook.com/mary/')
    learner_mary.save()
    learner_robert = Learner(first_name='Robert', last_name='Lee', dob=date(1999, 1, 2), occupation='developer',
                             social_link='https://www.facebook.com/robert/')
    learner_robert.save()

    learners = Learner.objects.all()
    print(learners)
    # Add Instructors
    instructor_yan = Instructor(first_name='Yan', last_name='Luo', dob=date(1962, 7, 16),
                                full_time=True,
                                total_learners=100)
    instructor_yan.save()
    instructor_joy = Instructor(first_name='Joy', last_name='Li', dob=date(1992, 1, 2),
                                full_time=False,
                                total_learners=100)
    instructor_joy.save()
    instructor_peter = Instructor(first_name='Peter', last_name='Chen', dob=date(1982, 5, 2),
                                  full_time=True,
                                  total_learners=100)
    instructor_peter.save()

    instructors = Instructor.objects.all()
    print(instructors)

    # Add Courses
    course_cloud_app = Course(name="Cloud Application Development with Database",
                              description="Develop and deploy application on cloud")
    course_cloud_app.save()
    course_python = Course(name="Introduction to Python",
                           description="Learn core concepts of Python and obtain hands-on experience via a capstone project")
    course_python.save()
    course_cloud_app.instructors.add(instructor_yan)
    course_cloud_app.instructors.add(instructor_joy)

    print(course_cloud_app.instructors.all())

    course_python.instructors.add(instructor_peter)
    courses = Course.objects.all()
    print(courses)

    james_cloud = Enrollment.objects.create(learner=learner_james, date_enrolled=date(2020, 8, 1),
                                            course=course_cloud_app, mode='audit')
    james_cloud.save()
    mary_cloud = Enrollment.objects.create(learner=learner_mary, date_enrolled=date(2020, 8, 2),
                                           course=course_cloud_app, mode='honor')
    mary_cloud.save()

    robert_python = Enrollment.objects.create(learner=learner_robert, date_enrolled=date(2020, 9, 2),
                                              course=course_python, mode='honor')
    robert_python.save()
    print(course_python.learners.all())

    project_orm = Project(name="Object-relational mapping project", grade=0.2, course=course_cloud_app)
    project_django = Project(name="Django full stack project", grade=0.2, course=course_cloud_app)
    project_python = Project(name="Python final project", grade=0.5, course=course_python)
    print(project_orm)
    print(project_orm.course)
    print(project_python.course)


clean_data()
populate_database()
