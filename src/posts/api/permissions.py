from rest_framework.permissions import BasePermission

class UserOwnerPermission(BasePermission):
    message = 'Allowed only for owner of post or for admins'

    def has_object_permission(self, request, view, post):
        return post.user.id == request.user.id or request.user.is_staff