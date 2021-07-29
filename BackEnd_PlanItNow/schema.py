import graphene
from graphene_django import DjangoObjectType

from plans.models import Plan


class PlanType(DjangoObjectType):
    class Meta:
        model = Plan
        fields = ('id',
                  'title',
                  'description',
                  'location',
                  'init_date',
                  'init_hour',
                  'end_hour',
                  'is_public')


class Query(graphene.ObjectType):
    all_plans = graphene.List(PlanType)

    @staticmethod
    def resolve_all_plans(root,info):
        return Plan.objects.all()


schema = graphene.Schema(query=Query)
