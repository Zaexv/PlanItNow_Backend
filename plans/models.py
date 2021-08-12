from django.db import models
from django.contrib.auth import get_user_model


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
    """Plan description to add additional information"""
    description = models.CharField(max_length=1024)
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
    """Picture plan URL"""
    url_plan_picture = models.CharField(max_length=512,null=True)



# TODO Develop the other models
class PlanParticipation(models.Model):
    pass
