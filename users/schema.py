from django.contrib.auth import get_user_model
from userprofiles.schema import UserProfileType
from userprofiles.models import UserProfile

import graphene
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('id',
                  'username',
                  'user_profile',
                  )


class CreateUser(graphene.Mutation):
    """Register a user in the backend platform. This will create a very basic userprofile with some data too"""
    user = graphene.Field(UserType)

    class Arguments:
        """Minimum arguments"""
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        """User profile related arguments"""
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        birth_date = graphene.Date(required=True)

    @staticmethod
    def mutate(self, info, username, password, email, first_name, last_name, birth_date):

        if not(username and password and email and first_name and last_name and birth_date):
            raise Exception("Missing required fields")

        user = get_user_model()(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()

        user_profile = UserProfile()
        user_profile.user = user
        user_profile.birth_date = birth_date
        user_profile.save()

        return CreateUser(user=user)


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    @staticmethod
    def resolve_users(self, info):
        return get_user_model().objects.all()

    @staticmethod
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
