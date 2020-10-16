# Django specific settings
import inspect
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.db import connection
# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Your application specific imports
from data.models import *
from datetime import date


def clean_data():
    # Delete all
    Enrollment.objects.all().delete()
    User.objects.all().delete()
    Learner.objects.all().delete()
    Instructor.objects.all().delete()
    Course.objects.all().delete()
    Project.objects.all().delete()


def populate_database():
    # Add user
    user = User(first_name='John', last_name='Doe', dob=date(1962, 7, 16))
    user.save()
    # Add Learners
    learner_james = Learner(first_name='James', last_name='Smith', dob=date(1982, 7, 16),
                            occupation='data_scientist',
                            social_link='https://www.linkedin.com/james/')
    learner_james.save()
    print(inspect.getmro(Learner))

    learner_mary = Learner(first_name='Mary', last_name='Smith', dob=date(1991, 6, 12), occupation='dba',
                           social_link='https://www.facebook.com/mary/')
    learner_mary.save()
    learner_robert = Learner(first_name='Robert', last_name='Lee', dob=date(1999, 1, 2), occupation='student',
                             social_link='https://www.facebook.com/robert/')
    learner_robert.save()
    learner_david = Learner(first_name='David', last_name='Smith', dob=date(1983, 7, 16),
                            occupation='developer',
                            social_link='https://www.linkedin.com/david/')
    learner_david.save()

    learner_john = Learner(first_name='John', last_name='Smith', dob=date(1986, 3, 16),
                            occupation='developer',
                            social_link='https://www.linkedin.com/john/')
    learner_john.save()

    # Add Instructors
    instructor_yan = Instructor(first_name='Yan', last_name='Luo', dob=date(1962, 7, 16),
                                full_time=True,
                                total_learners=30050)
    instructor_yan.save()
    print(inspect.getmro(Instructor))

    instructor_joy = Instructor(first_name='Joy', last_name='Li', dob=date(1992, 1, 2),
                                full_time=False,
                                total_learners=10040)
    instructor_joy.save()
    instructor_peter = Instructor(first_name='Peter', last_name='Chen', dob=date(1982, 5, 2),
                                  full_time=True,
                                  total_learners=2002)
    instructor_peter.save()

    # Add Courses
    course_cloud_app = Course(name="Cloud Application Development with Database",
                              description="Develop and deploy application on cloud")
    course_cloud_app.save()
    course_python = Course(name="Introduction to Python",
                           description="Learn core concepts of Python and obtain hands-on "
                                       "experience via a capstone project")
    course_python.save()
    course_cloud_app.instructors.add(instructor_yan)
    course_cloud_app.instructors.add(instructor_joy)

    course_python.instructors.add(instructor_peter)

    james_cloud = Enrollment.objects.create(learner=learner_james, date_enrolled=date(2020, 8, 1),
                                            course=course_cloud_app, mode='audit')
    james_cloud.save()
    mary_cloud = Enrollment.objects.create(learner=learner_mary, date_enrolled=date(2020, 8, 2),
                                           course=course_cloud_app, mode='honor')
    mary_cloud.save()
    david_cloud = Enrollment.objects.create(learner=learner_david, date_enrolled=date(2020, 8, 5),
                                           course=course_cloud_app, mode='honor')
    david_cloud.save()
    david_john = Enrollment.objects.create(learner=learner_john, date_enrolled=date(2020, 8, 5),
                                            course=course_cloud_app, mode='audit')
    david_john.save()

    robert_python = Enrollment.objects.create(learner=learner_robert, date_enrolled=date(2020, 9, 2),
                                              course=course_python, mode='honor')
    robert_python.save()

    project_orm = Project(name="Object-relational mapping project", grade=0.2, course=course_cloud_app)
    project_django = Project(name="Django full stack project", grade=0.2, course=course_cloud_app)
    project_python = Project(name="Python final project", grade=0.5, course=course_python)

    print("Course: {}".format(course_cloud_app))
    print("Course instructors: {}".format(course_cloud_app.instructors.all()))
    print("Course learners: {}".format(course_cloud_app.learners.all()))
    print("Course project: {}".format(project_orm.name))


def simple_queries():
    # Find a single instructor
    instructor_yan = Instructor.objects.get(first_name="Yan")
    print(instructor_yan)
    try:
        instructor_andy = Instructor.objects.get(first_name="Andy")
    except Instructor.DoesNotExist:
        print("Instructor Andy doesn't exist")

    # Find students with last name "Smith"
    learners_smith = Learner.objects.filter(last_name="Smith")
    print(learners_smith)

    # Find all full time instructors
    full_time_instructors = Instructor.objects.exclude(full_time=False)
    print(full_time_instructors)

    # Find all full time instructors with First Name starts with `Y` and learners count greater than 30000
    full_time_instructors = Instructor.objects.exclude(full_time=False).filter(total_learners__gt=30000).\
        filter(first_name__startswith='Y')
    print(full_time_instructors)

    # Slicing, OFFSET=1, LIMIT=2
    learners = Learner.objects.all()[1:3]
    print(learners)

    # Order by
    learners = Learner.objects.order_by('dob')
    print(learners)


def span_relationship_queries():
    # Many-to-One relationship
    # Find the instructors of Cloud app dev course
    instructors = Instructor.objects.filter(course__name__contains='Cloud')
    print(instructors)
    # Find courses instructed by 'Yan'
    courses = Course.objects.filter(instructors__first_name='Yan')
    print(courses)
    # Check the occupations of the courses taught by instructor Yan
    courses = Course.objects.filter(instructors__first_name='Yan')
    occupation_list = set()
    for course in courses:
        for learner in course.learners.all():
            occupation_list.add(learner.occupation)
    print(occupation_list)
    # Many-to-Many relationship
    # Learners and Course Enrollment
    # Check which courses developers are enrolled in year Aug, 2020 with Honer
    enrollments = Enrollment.objects.filter(date_enrolled__month=8,
                                            date_enrolled__year=2020,
                                            learner__occupation='developer')
    courses_for_developers = set()
    for enrollment in enrollments:
        course = enrollment.course
        courses_for_developers.add(course.name)
    print(courses_for_developers)


def update_data():
    # Update field in one model
    learner_david = Learner.objects.get(first_name='David')
    print(learner_david)
    learner_david.social_link = "https://www.linkedin.com/david2/"
    learner_david.save()
    learner_david = Learner.objects.get(first_name="David")
    print(learner_david)

    # Add a learner to course
    course_python = Course.objects.get(name__contains='Python')
    print(course_python.learners.all())
    learner_joe = Learner(first_name='Joe', last_name='Smith', dob=date(1985, 3, 16),
                          occupation='developer',
                          social_link='https://www.linkedin.com/david/')
    learner_joe.save()
    course_python.learners.add(learner_joe)
    print(course_python.learners.all())

    # Delete its enrollment first
    # Delete the learner
    joe_enrollments = Enrollment.objects.filter(learner__first_name="Joe")
    print(joe_enrollments)
    joe_enrollments.delete()
    learner_joe.delete()
    print(Learner.objects.all())
    print(course_python.learners.all())


clean_data()
populate_database()
simple_queries()
span_relationship_queries()
update_data()
