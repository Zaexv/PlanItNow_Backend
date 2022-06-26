from django.contrib.auth import get_user_model
from django.db import models

from userprofiles.models import UserProfile


# PlanModel
class Plan(models.Model):
    # Relations
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE)

    # TODO Add Participations

    # Attributes
    """Plan Title"""
    title = models.CharField(max_length=256, null=False)
    """Plan English Title for recommendation purpose"""
    english_title = models.CharField(max_length=256, null=False, default="pending translation")
    """Plan description to add additional information"""
    description = models.CharField(max_length=1024)
    """Plan english description for recommendation purpose"""
    english_description = models.CharField(max_length=1024,default="pending translation")
    """Plan location in text format, where is the plan going to be?"""
    location = models.CharField(max_length=128, null=False)
    """When does the plan begins?"""
    init_date = models.DateField(null=False)
    """What time do the plan begin?"""
    init_hour = models.TimeField(null=False)
    """What time do the plan ends?"""
    end_hour = models.TimeField(null=False)
    """Is the plan for everyone or just for friends?
        if is_public everyone is able to see the plan
        otherwise only friends and invited people are able to see it
    """
    is_public = models.BooleanField(null=True)
    """Max participants in a plan"""
    max_participants = models.IntegerField(blank=True, null=True, default=5)
    """Picture plan URL"""
    url_plan_picture = models.CharField(max_length=512, null=True)

    class Meta:
        ordering = ('init_date',
                    'init_hour',
                    'end_hour')


class PlanParticipation(models.Model):
    """Creation date of the request"""
    created_at = models.DateTimeField(auto_now_add=True)
    """Last time the object was updated"""
    updated_at = models.DateTimeField(auto_now=True)
    """Stores the user who is participating in plan"""
    participant_user = models.ForeignKey(
        UserProfile, related_name="participant_user", on_delete=models.CASCADE,
    )
    """Stores the plan on which user is participating"""
    participating_plan = models.ForeignKey(
        Plan, related_name="participating_plan", on_delete=models.CASCADE,
    )
    """Did the user like the plan?"""
    user_likes = models.BooleanField(default=True)

    def delete_participation(self):
        """Delete this participation"""
        self.delete()
