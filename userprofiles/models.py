from django.db import models
from django.contrib.auth import get_user_model
# from phonenumber_field.modelfields import PhoneNumberField

 #TODO Fix PhoneNumbers
class UserProfile(models.Model):
    """This a reference. This is just for consistency purposes."""
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    """User phone number used in some queries and further authentication"""
   # phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    """Birth date of the user"""
    birth_date = models.DateField(null=True)
    """Some user introduced extra information :)"""
    biography = models.CharField(max_length=1024)
    """The common residence of the user"""
    residence = models.CharField(max_length=256)
    """URL of Profile Picture"""
    url_profile_picture = models.CharField(max_length=512)
