from datetime import date

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q


# from phonenumber_field.modelfields import PhoneNumberField


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

    def get_recommended_plans(self):
        today = date.today()
        friends_ids = self.friends.values_list('id', flat=True)
        return self.user_distance.filter(
            Q(plan__init_date__gte=today), Q(distance__gte=0.0),
            (
                    Q(plan__owner__id=self.user.id) |
                    Q(plan__is_public=True) |
                    Q(plan__owner__id__in=friends_ids)
            ),
            ).order_by(
            'distance')[:10]
