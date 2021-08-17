from friendship.models import FriendRequest
from friendship.models import FriendRequestStatus
from userprofiles.models import UserProfile

import graphene
from graphene_django import DjangoObjectType


class FriendRequestType(DjangoObjectType):
    class Meta:
        model = FriendRequest
        fields = ('id',
                  'from_user',
                  'to_user',
                  'request_status',
                  'is_accepted',
                  'created_at')


class SendFriendRequest(graphene.Mutation):
    friend_request = graphene.Field(FriendRequestType)

    class Arguments:
        to_username = graphene.String(required=True)

    @staticmethod
    def mutate(self, info, to_username):
        logged_user = info.context.user
        if logged_user.is_anonymous:
            raise Exception("Not logged in!")
        to_user = UserProfile.objects.get(user__username=to_username)
        from_user = UserProfile.objects.get(pk=logged_user.id)

        if not to_user or not from_user:
            raise Exception("Error: Cannot find user to request")

        if FriendRequest.objects.filter(to_user=to_user, from_user=from_user) \
                or FriendRequest.objects.filter(to_user=from_user, from_user=to_user):
            raise Exception("Error: Friend Request Already Exists")

        friend_request = FriendRequest(to_user=to_user, from_user=from_user)
        friend_request.save()

        return SendFriendRequest(friend_request=friend_request)


class AcceptFriendRequest(graphene.Mutation):
    friend_request = graphene.Field(FriendRequestType)

    class Arguments:
        fr_id = graphene.Int(required=True)

    @staticmethod
    def mutate(self, info, fr_id):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Must be logged to accept FriendRequest')

        friend_request = FriendRequest.objects.get(pk=fr_id)

        if friend_request.to_user.id != user.id:
            raise Exception('Cannot accept other user requests!')

        friend_request.accept_friend_request()

        return AcceptFriendRequest(friend_request=friend_request)


class RejectFriendRequest(graphene.Mutation):
    friend_request = graphene.Field(FriendRequestType)

    class Arguments:
        fr_id = graphene.Int(required=True)

    @staticmethod
    def mutate(self, info, fr_id):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Must be logged to reject a FriendRequest')

        friend_request = FriendRequest.objects.get(pk=fr_id)

        if friend_request.to_user.id != user.id:
            raise Exception('Cannot reject other user requests!')

        friend_request.reject_friend_request()

        return RejectFriendRequest(friend_request=friend_request)


class Query(graphene.ObjectType):
    received_friend_requests = graphene.List(FriendRequestType)
    sent_friend_requests = graphene.List(FriendRequestType)

    @staticmethod
    def resolve_received_friend_requests(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return FriendRequest.objects.filter(to_user=user.id)

    @staticmethod
    def resolve_sent_friend_requests(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return FriendRequest.objects.filter(from_user=user.id,
                                            is_accepted=False,
                                            )


class Mutation(graphene.ObjectType):
    send_friend_request = SendFriendRequest.Field()
    accept_friend_request = AcceptFriendRequest.Field()
    reject_friend_request = RejectFriendRequest.Field()
