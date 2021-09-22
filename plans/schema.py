import graphene

from datetime import date
from graphene_django import DjangoObjectType
from plans.models import Plan
from plans.models import PlanParticipation

from userprofiles.models import UserProfile
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
                  'max_participants',
                  'url_plan_picture',
                  'owner',
                  'participating_plan')


class PlanParticipationType(DjangoObjectType):
    class Meta:
        model = PlanParticipation
        fields = ('id',
                  'participating_plan',
                  'participant_user')


class CreatePlan(graphene.Mutation):
    plan = graphene.Field(PlanType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        location = graphene.String(required=True)
        init_date = graphene.Date(required=True)
        init_hour = graphene.Time(required=True)
        end_hour = graphene.Time(required=True)
        max_participants = graphene.Int(required=False)
        is_public = graphene.Boolean(required=False)
        url_plan_picture = graphene.String(required=False)
        max_participants = graphene.Int(required=False)

    @staticmethod
    def mutate(self,
               info,
               title,
               description,
               location,
               init_date,
               init_hour,
               end_hour,
               max_participants=5,
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
                    max_participants=max_participants,
                    is_public=is_public,
                    url_plan_picture=url_plan_picture)
        plan.owner = user
        plan.save()
        return CreatePlan(plan=plan)


class EditPlan(graphene.Mutation):
    plan = graphene.Field(PlanType)

    class Arguments:
        plan_id = graphene.Int(required=True)
        title = graphene.String(required=False)
        description = graphene.String(required=False)
        location = graphene.String(required=False)
        init_date = graphene.Date(required=False)
        init_hour = graphene.Time(required=False)
        end_hour = graphene.Time(required=False)
        max_participants = graphene.Int(required=False)
        is_public = graphene.Boolean(required=False)
        url_plan_picture = graphene.String(required=False)
        max_participants = graphene.Int(required=False)

    @staticmethod
    def mutate(self,
               info,
               plan_id,
               title,
               description,
               location,
               init_date,
               init_hour,
               end_hour,
               max_participants,
               is_public=False,
               url_plan_picture=""):
        user = info.context.user

        if user.is_anonymous:
            print("Error, user not logged")
            raise Exception('Must be logged to create a plan')

        plan = Plan.objects.get(pk=plan_id)

        if plan.owner.id != user.id:
            print('Error, not the same user')
            raise Exception('MUST BE THE CREATOR TO DELETE THIS PLAN')

        if title: plan.title = title
        if description: plan.description = description
        if location: plan.location = location
        if init_date: plan.init_date = init_date
        if init_hour: plan.init_hour = init_hour
        if end_hour: plan.end_hour = end_hour
        if max_participants: plan.max_participants = max_participants
        if is_public: plan.is_public = is_public
        if url_plan_picture: plan.url_plan_picture = url_plan_picture

        plan.save()

        return EditPlan(plan=plan)


class DeletePlan(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    @staticmethod
    def mutate(self, info, id):
        user = info.context.user

        if user.is_anonymous:
            print('Error, user not logged')
            raise Exception('Must be logged to DELETE a plan')

        plan = Plan.objects.get(pk=id)

        if plan.owner.id == user.id:
            plan.delete()
        else:
            print('Error, not the same user')
            raise Exception('MUST BE THE CREATOR TO DELETE THIS PLAN')

        return DeletePlan(ok=True)


class ParticipateInPlan(graphene.Mutation):
    """In the case that it already exists a participation, it will be destroyed"""
    plan_participation = graphene.Field(PlanParticipationType)

    class Arguments:
        plan_id = graphene.Int(required=True)

    @staticmethod
    def mutate(self, info, plan_id):
        user = info.context.user

        if user.is_anonymous:
            print('Error, user not logged')
            raise Exception('Must be logged to participate in a plan')

        plan = Plan.objects.get(pk=plan_id)

        participation = plan.participating_plan.filter(participant_user__pk=user.id)

        if participation:
            participation[0].delete_participation()
            result = None
        else:
            if plan.participating_plan.count() >= plan.max_participants:
                raise Exception('The plan is full')
            to_userprofile = UserProfile.objects.get(pk=user.id)
            result = PlanParticipation(participating_plan=plan, participant_user=to_userprofile)
            result.save()

        return ParticipateInPlan(plan_participation=result)


class Query(graphene.ObjectType):
    all_plans = graphene.List(PlanType, is_diary=graphene.Boolean(required=False, default_value=False))
    detailed_plan = graphene.Field(PlanType, id=graphene.Int(required=True))
    recommended_or_search = graphene.List(PlanType, search_string=graphene.String(required=False))

    @staticmethod
    def resolve_detailed_plan(root, info, id):
        if info.context.user.is_anonymous:
            raise Exception("Not logged in!")
        return Plan.objects.get(pk=id)

    @staticmethod
    def resolve_all_plans(root, info, is_diary):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")

        profile = UserProfile.objects.get(pk=user.id)
        today = date.today()
        if is_diary:
            return Plan.objects.filter((
                    Q(owner__id=user.id) |
                    Q(participating_plan__participant_user=profile)
            ),
                (
                    Q(init_date__lte=today)
                )
            ).distinct().order_by('-init_date', '-init_hour', '-end_hour')
        else:
            friend_ids = profile.friends.values_list('id', flat=True)
            return Plan.objects.filter((
                    Q(owner__id=user.id) |
                    Q(participating_plan__participant_user=profile)
            ),
                (
                    Q(init_date__gte=today)
                )
            ).distinct()

    @staticmethod
    def resolve_recommended_or_search(root, info, search_string):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")

        profile = UserProfile.objects.get(pk=user.id)
        friend_ids = profile.friends.values_list('id', flat=True)
        today = date.today()
        if search_string:
            result = Plan.objects.filter(
                (
                        Q(owner__id=user.id) |
                        Q(is_public=True) |
                        Q(owner__id__in=friend_ids)
                ),
                (
                        Q(title__icontains=search_string) |
                        Q(description__icontains=search_string)
                ),
                (
                    Q(init_date__gte=today)
                ),
                (
                    Q(max_participants__gte=1)
                )
            )
        else:
            recommendation = profile.get_recommended_plans()
            recommendation_plans_ids = recommendation.values_list('plan', flat=True)
            result = Plan.objects.filter(
                Q(owner__id=user.id) |
                Q(is_public=True) |
                Q(owner__id__in=friend_ids),
                (
                    Q(init_date__gte=today)
                ),
                (
                    Q(max_participants__gte=1)
                ),
            ).exclude(id__in=recommendation_plans_ids)
            result = list(result)
            for distance in recommendation:
                result.insert(0, distance.plan)
        return result


class Mutation(graphene.ObjectType):
    create_plan = CreatePlan.Field()
    edit_plan = EditPlan.Field()
    delete_plan = DeletePlan.Field()
    participate_in_plan = ParticipateInPlan.Field()
