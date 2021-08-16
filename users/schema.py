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
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @staticmethod
    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        # Todo añadir user profile a la hora de crear usuario
        user.set_password(password)
        user.save()

        user_profile = UserProfile()
        user_profile.user = user
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
