from datetime import datetime

from django.test import TestCase
# Create your tests here.
from userprofiles.models import UserProfile
from users.schema import CreateUser


def inc(x):
    return x + 2


def test_answer():
    assert inc(3) == 5

def test_user():
    CreateUser.mutate("test_user", "test_password", "Test_email","test_name", datetime.today())
    my_profile = UserProfile.objects.get(user__id=1)


