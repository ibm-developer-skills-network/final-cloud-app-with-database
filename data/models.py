import sys
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()


# User model
class User(models.Model):
    first_name = models.CharField(null=False, max_length=30, default='john')
    last_name = models.CharField(null=False, max_length=30, default='doe')
    dob = models.DateField(null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


# Learner model
class Learner(User):
    STUDENT = 'STU'
    DEVELOPER = 'DEV'
    DATA_SCIENTIST = 'DS'
    DATABASE_ADMIN = 'DBA'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=3,
        choices=OCCUPATION_CHOICES,
        default=STUDENT,
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.first_name + "," + self.last_name + ", " + self.occupation + ", " + self.social_link


