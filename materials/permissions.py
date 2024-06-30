from rest_framework.permissions import BasePermission


class IsModeratorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators_course').exists()


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
