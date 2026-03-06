from django.utils.timezone import now, timedelta
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and not request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CanEditSomeTime(BasePermission):
    def has_object_permission(self, request, view, obj):
        passed_time = now() - obj.updated_at
        return passed_time >= timedelta(minutes=1)

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_staff
            and request.method != "POST"
        )