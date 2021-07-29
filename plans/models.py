from django.db import models


#PlanModel
class Plan(models.Model):
    title = models.CharField(max_length=256, null=False)
    description = models.CharField(max_length=1024)
    location = models.CharField(max_length=128, null=False)
    init_date = models.DateField(null=False)
    init_hour = models.TimeField(null=False)
    end_hour = models.TimeField(null=False)
    is_public = models.BooleanField()

#TODO Develop the other models