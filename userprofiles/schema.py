from userprofiles.models import UserProfile
from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = ('id',
                  'public_username',
                  'user',
                  'birth_date',
                  'biography',
                  'residence',
                  'url_profile_picture',
                  )


class EditProfile(graphene.Mutation):
    user_profile = graphene.Field(UserProfileType)

    class Arguments:
        public_username = graphene.String(required=False)
        biography = graphene.String(required=False)
        residence = graphene.String(required=False)
        url_profile_picture = graphene.String(required=False)

    @staticmethod
    def mutate(self, info, public_username=None, biography=None, residence=None, url_profile_picture=None):
        user = info.context.user

        if user.is_anonymous:
            print('Error, user not logged')
            raise Exception('Must be logged to Edit your Profile')

        db_user = get_user_model().objects.get(pk=user.id)
        profile = db_user.user_profile

        if public_username:
            profile.public_username = public_username
        if biography:
            profile.biography = biography
        if residence:
            profile.residence = residence
        if url_profile_picture:
            profile.url_profile_picture = url_profile_picture

        profile.save()
        return EditProfile(user_profile=profile)


class Query(graphene.ObjectType):
    my_friends = graphene.List(UserProfileType)

    @staticmethod
    def resolve_my_friends(self, info):
        if info.context.user.is_anonymous:
            raise Exception("You must be logged to see your friends!")
        my_id = info.context.user.id
        my_profile = UserProfile.objects.get(user__id=my_id)
        return my_profile.friends.all()


class Mutation(graphene.ObjectType):
    edit_profile = EditProfile.Field()
