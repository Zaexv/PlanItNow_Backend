from userprofiles.models import UserProfile
from django.db import models
from enum import Enum


class FriendRequestStatus(Enum):
    """Stores the different friendship request status"""
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)


class FriendRequest(models.Model):
    """Creation date of the request"""
    created_at = models.DateTimeField(auto_now_add=True)
    """Last time the object was updated"""
    updated_at = models.DateTimeField(auto_now=True)
    """Stores the user who is sending the Friendship Request"""
    from_user = models.ForeignKey(
        UserProfile, related_name="friends_requests_from_user", on_delete=models.CASCADE,
    )
    """Stores the user which is being sent the Friendship Request"""
    to_user = models.ForeignKey(
        UserProfile, related_name="friends_requests_to_user", on_delete=models.CASCADE,
    )
    """Is the friendship accepted?"""
    is_accepted = models.BooleanField(default=False)
    """Status of the friend Request regarding ENUM"""
    request_status = models.CharField(choices=FriendRequestStatus.choices(),
                                      default=FriendRequestStatus.PENDING.value,
                                      max_length=64)

    def accept_friend_request(self):
        """Accepts this friend request, adding as a friend to both users """
        if self.request_status != FriendRequestStatus.REJECTED.value:
            self.is_accepted = True
            self.request_status = FriendRequestStatus.ACCEPTED.value
            self.from_user.friends.add(self.to_user)
            self.from_user.save()
            self.to_user.friends.add(self.from_user)
            self.to_user.save()
        self.save()

    def reject_friend_request(self):
        """Rejects friendship from one of both users. This will not allow to perform any further request of
        friendship """
        self.is_accepted = False
        self.request_status = FriendRequestStatus.REJECTED
        self.save()

    def delete_friendship(self):
        """Delete this friendship as they do not want to be friends anymore"""
        self.from_user.friends.remove(self.to_user)
        self.from_user.save()
        self.to_user.friends.remove(self.from_user)
        self.to_user.save()
        self.delete()
