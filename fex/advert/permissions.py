from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsOwnerOnlyForAdvertFile(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
    	return obj.advert_id.author == request.user


class IsStaffOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
    	return request.user.is_staff == True


class IsOwnerOnlyForReplyFile(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
    	return obj.reply_id.author == request.user

