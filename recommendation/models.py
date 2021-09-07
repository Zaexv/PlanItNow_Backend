from django.db import models
from plans.models import Plan
from userprofiles.models import UserProfile


class Distance(models.Model):
    """Creation date of the distance"""
    created_at = models.DateTimeField(auto_now_add=True)
    """Last time the object was updated"""
    updated_at = models.DateTimeField(auto_now=True)

    """First plan created"""
    plan1 = models.ForeignKey(
        Plan, related_name="plan1", on_delete=models.CASCADE,
    )

    """Newer plan"""
    plan2 = models.ForeignKey(
        Plan, related_name="plan2", on_delete=models.CASCADE,
    )

    """Distance between plans. This is a calculated value. -1.0 is the non active value"""
    distance = models.FloatField(default=-1.0)


class UserDistance(models.Model):
    """Creation date of the distance"""
    created_at = models.DateTimeField(auto_now_add=True)
    """Last time the object was updated"""
    updated_at = models.DateTimeField(auto_now=True)

    """First plan created"""
    user = models.ForeignKey(
        UserProfile, related_name="user_distance", on_delete=models.CASCADE,
    )

    """Newer plan"""
    plan = models.ForeignKey(
        Plan, related_name="plan_user_distance", on_delete=models.CASCADE,
    )

    """Distance between user and plan. This is a calculated value. -1.0 is the non active value"""
    distance = models.FloatField(default=-1.0)


class Lemma(models.Model):
    """Creation date of the lemma"""
    created_at = models.DateTimeField(auto_now_add=True)
    """Last time the object was updated"""
    updated_at = models.DateTimeField(auto_now=True)

    """String of the lemma in english"""
    lemma = models.CharField(primary_key=True, max_length=128)

    """The plans containing this lemma"""
    corresponding_plans = models.ManyToManyField(Plan)
