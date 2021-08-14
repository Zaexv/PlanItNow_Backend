from userprofiles.models import UserProfile

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


class Query(graphene.ObjectType):
    my_friends = graphene.List(UserProfileType)

    @staticmethod
    def resolve_my_friends(self, info):
        my_id = info.context.user.id
        my_profile = UserProfile.objects.get(pk=my_id)
        return my_profile.friends.all()
