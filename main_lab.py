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
    # Delete all data to start from fresh
    Enrollment.objects.all().delete()
    User.objects.all().delete()
    Learner.objects.all().delete()
    Instructor.objects.all().delete()
    Course.objects.all().delete()
    Lesson.objects.all().delete()


def populate_instructors():
    # Add users
    user_john = User(first_name='John', last_name='Doe', dob=date(1962, 7, 16))
    user_john.save()
    # Add Learners
    instructor_john = Instructor(full_time=True,
                                total_learners=30050)
    instructor_john.user = user_john
    instructor_john.save()

    instructor_yan = Instructor(first_name='Yan', last_name='Luo', dob=date(1962, 7, 16),
                                full_time=True,
                                total_learners=30050)
    instructor_yan.save()

    instructor_joy = Instructor(first_name='Joy', last_name='Li', dob=date(1992, 1, 2),
                                full_time=False,
                                total_learners=10040)
    instructor_joy.save()
    instructor_peter = Instructor(first_name='Peter', last_name='Chen', dob=date(1982, 5, 2),
                                  full_time=True,
                                  total_learners=2002)
    instructor_peter.save()


def populate_learners():
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


def populate_courses():
    # Add Courses
    course_cloud_app = Course(name="Cloud Application Development with Database",
                              description="Develop and deploy application on cloud")
    course_cloud_app.save()
    course_python = Course(name="Introduction to Python",
                           description="Learn core concepts of Python and obtain hands-on "
                                       "experience via a capstone project")
    course_python.save()


def populate_lessons():
    # Add lessons
    lession1 = Lesson(title='Lesson 1', content="Object-relational mapping project")
    lession1.save()
    lession2 = Lesson(title='Lesson 2', content="Django full stack project")
    lession2.save()


def query_courses():
    #Find all courses
    courses = Course.objects.all()
    print(courses)


def query_instructors():
    # Find a single instructor
    instructor_yan = Instructor.objects.get(first_name="Yan")
    print(instructor_yan)
    try:
        instructor_andy = Instructor.objects.get(first_name="Andy")
    except Instructor.DoesNotExist:
        print("Instructor Andy doesn't exist")

    # Find all part time instructors
    part_time_instructors = Instructor.objects.filter(full_time=False)
    print("Part time instructors: ")
    print(part_time_instructors)

    # Find all full time instructors with First Name starts with `Y` and learners count greater than 30000
    full_time_instructors = Instructor.objects.exclude(full_time=False).filter(total_learners__gt=30000).\
        filter(first_name__startswith='Y')
    print("Full time instructors: ")
    print(full_time_instructors)

    full_time_instructors = Instructor.objects.filter(full_time=True, total_learners__gt=30000,
                                                      first_name__startswith='Y')
    print("Full time instructors: ")
    print(full_time_instructors)


def query_lessons():
    lessons = Lesson.objects.filter(title__startswith='Lesson')
    print(lessons)


def query_learners():
    # Find a single instructor
    instructor_yan = Instructor.objects.get(first_name="Yan")
    print(instructor_yan)
    try:
        instructor_andy = Instructor.objects.get(first_name="Andy")
    except Instructor.DoesNotExist:
        print("Instructor Andy doesn't exist")

    # Find all part time instructors
    part_time_instructors = Instructor.objects.filter(full_time=False)
    print("Part time instructors: ")
    print(part_time_instructors)

    # Find all full time instructors with First Name starts with `Y` and learners count greater than 30000
    full_time_instructors = Instructor.objects.exclude(full_time=False).filter(total_learners__gt=30000).\
        filter(first_name__startswith='Y')
    print("Full time instructors")
    print(full_time_instructors)

    full_time_instructors = Instructor.objects.filter(full_time=True, total_learners__gt=30000,
                                                      first_name__startswith='Y')
    print("Full time instructors")
    print(full_time_instructors)


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
    course = Course.objects.get(name='Introduction to Python')
    learners = course.learners.all()
    print(learners.query)
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

    # Related objects
    print("One-To-One")
    learner_david = Learner.objects.get(first_name="David")
    print(learner_david.user_ptr)
    user_david = User.objects.get(first_name="David")
    print(user_david.learner)

    print("One-To-Many")
    lesson1 = Lesson.objects.get(title__contains="Lesson 1")
    print(lesson1.course)
    course = Course.objects.get(name__contains='Cloud')
    print(course)
    print(course.lesson_set.all())

    print("Many-To-Many")
    instructor_yan = Instructor.objects.get(first_name='Yan')
    print(instructor_yan.course_set.all())
    course = Course.objects.get(name__contains='Cloud')
    print(course.instructors.all())


def populate_course_instructor_relationships():
    # Get related instructors
    instructor_yan = Instructor.objects.get(first_name='Yan')
    instructor_joy = Instructor.objects.get(first_name='Joy')
    instructor_peter = Instructor.objects.get(first_name='Peter')

    # Get related courses
    course_cloud_app = Course.objects.get(name__contains='Cloud')
    course_python = Course.objects.get(name__contains='Python')

    # Add instructors to courses
    course_cloud_app.instructors.add(instructor_yan)
    course_cloud_app.instructors.add(instructor_joy)
    course_python.instructors.add(instructor_peter)

    # Get related learners
    learner_james = Learner.objects.get(first_name='James')
    learner_mary = Learner.objects.get(first_name='Mary')
    learner_david = Learner.objects.get(first_name='David')
    learner_john = Learner.objects.get(first_name='John')
    learner_robert = Learner.objects.get(first_name='Robert')

    # Add enrollment
    james_cloud = Enrollment.objects.create(learner=learner_james, date_enrolled=date(2020, 8, 1),
                                            course=course_cloud_app, mode='audit')
    james_cloud.save()
    mary_cloud = Enrollment.objects.create(learner=learner_mary, date_enrolled=date(2020, 8, 2),
                                         course=course_cloud_app, mode='honor')
    mary_cloud.save()
    david_cloud = Enrollment.objects.create(learner=learner_david, date_enrolled=date(2020, 8, 5),
                                            course=course_cloud_app, mode='honor')
    david_cloud.save()
    david_cloud = Enrollment.objects.create(learner=learner_john, date_enrolled=date(2020, 8, 5),
                                           course=course_cloud_app, mode='audit')
    david_cloud.save()
    robert_python = Enrollment.objects.create(learner=learner_robert, date_enrolled=date(2020, 9, 2),
                                              course=course_python, mode='honor')
    robert_python.save()


def populate_course_enrollment_relationships():

    # Get related courses
    course_cloud_app = Course.objects.get(name__contains='Cloud')
    course_python = Course.objects.get(name__contains='Python')

    # Get related learners
    learner_james = Learner.objects.get(first_name='James')
    learner_mary = Learner.objects.get(first_name='Mary')
    learner_david = Learner.objects.get(first_name='David')
    learner_john = Learner.objects.get(first_name='John')
    learner_robert = Learner.objects.get(first_name='Robert')

    # Add enrollment
    james_cloud = Enrollment.objects.create(learner=learner_james, date_enrolled=date(2020, 8, 1),
                                            course=course_cloud_app, mode='audit')
    james_cloud.save()
    mary_cloud = Enrollment.objects.create(learner=learner_mary, date_enrolled=date(2020, 8, 2),
                                         course=course_cloud_app, mode='honor')
    mary_cloud.save()
    david_cloud = Enrollment.objects.create(learner=learner_david, date_enrolled=date(2020, 8, 5),
                                            course=course_cloud_app, mode='honor')
    david_cloud.save()
    david_cloud = Enrollment.objects.create(learner=learner_john, date_enrolled=date(2020, 8, 5),
                                           course=course_cloud_app, mode='audit')
    david_cloud.save()
    robert_python = Enrollment.objects.create(learner=learner_robert, date_enrolled=date(2020, 9, 2),
                                              course=course_python, mode='honor')
    robert_python.save()


clean_data()
populate_courses()
populate_instructors()
populate_learners()
populate_lessons()

query_courses()
query_instructors()
query_learners()
query_lessons()

populate_course_instructor_relationships()
populate_course_enrollment_relationships()

span_relationship_queries()
#update_data()