import graphene

from graphene_django import DjangoObjectType
from plans.models import Plan
from django.db.models import Q


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
                  'is_public',
                  'url_plan_picture',
                  'owner')


class CreatePlan(graphene.Mutation):
    plan = graphene.Field(PlanType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        location = graphene.String(required=True)
        init_date = graphene.Date(required=True)
        init_hour = graphene.Time(required=True)
        end_hour = graphene.Time(required=True)
        is_public = graphene.Boolean(required=False)
        url_plan_picture = graphene.String(required=False)

    @staticmethod
    def mutate(self,
               info,
               title,
               description,
               location,
               init_date,
               init_hour,
               end_hour,
               is_public=False,
               url_plan_picture=""):
        user = info.context.user

        if user.is_anonymous:
            print("Error, user not logged")
            raise Exception('Must be logged to create a plan')

        plan = Plan(title=title,
                    description=description,
                    location=location,
                    init_date=init_date,
                    init_hour=init_hour,
                    end_hour=end_hour,
                    is_public=is_public,
                    url_plan_picture=url_plan_picture)
        plan.owner = user
        plan.save()
        return CreatePlan(plan=plan)


class DeletePlan(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    @staticmethod
    def mutate(self,
               info,
               id):
        user = info.context.user

        if user.is_anonymous:
            print("Error, user not logged")
            raise Exception('Must be logged to DELETE a plan')

        plan = Plan.objects.get(pk=id)

        if plan.owner.id == user.id:
            plan.delete()
        else:
            print("Error, not the same user")
            raise Exception('MUST BE THE CREATOR TO DELETE THIS PLAN')

        return DeletePlan(ok=True)


class Query(graphene.ObjectType):
    all_plans = graphene.List(PlanType)
    detailed_plan = graphene.Field(PlanType, id=graphene.Int(required=True))

    @staticmethod
    def resolve_detailed_plan(root, info, id):
        if info.context.user.is_anonymous:
            raise Exception("Not logged in!")
        return Plan.objects.get(pk=id)

    @staticmethod
    def resolve_all_plans(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return Plan.objects.filter(
            Q(owner__id=user.id) | Q(is_public=True)
        ).order_by('-init_date',
                   '-init_hour',
                   '-end_hour')


class Mutation(graphene.ObjectType):
    create_plan = CreatePlan.Field()
    delete_plan = DeletePlan.Field()
