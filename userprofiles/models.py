from django.db import models
from django.contrib.auth import get_user_model


# from phonenumber_field.modelfields import PhoneNumberField

# TODO Fix PhoneNumbers
class UserProfile(models.Model):
    """Public username. You can change this whenever you want"""
    public_username = models.CharField(max_length=128, default="No Username")
    """This a reference. This is just for consistency purposes."""
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name="user_profile")
    """User phone number used in some queries and further authentication"""
    # phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    """Birth date of the user"""
    birth_date = models.DateField(null=True, blank=True)
    """Some user introduced extra information :)"""
    biography = models.CharField(max_length=1024, default="No biography")
    """The common residence of the user"""
    residence = models.CharField(max_length=256, default="No residence")
    """URL of Profile Picture"""
    url_profile_picture = models.CharField(max_length=512, default="No profile Picture")
    """Friends of given User"""
    friends = models.ManyToManyField("UserProfile", blank=True)
