# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Your application specific imports
from data.models import *
from datetime import date


# Delete all
User.objects.all().delete()
Learner.objects.all().delete()

#Add user
user = User(first_name='Yan', last_name='Luo', dob=date(1962, 7, 16))
user.save()



# Application logic
first_user = User.objects.all()[0]
print(first_user)

learner = Learner(first_name='learner', last_name='learner', dob=date(1962, 7, 16), occupation='DBA',
                  social_link='https://www.linkedin.com/feed/')
learner.save()


first_learner = Learner.objects.all()[0]
print(first_learner)