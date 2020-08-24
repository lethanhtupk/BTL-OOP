from rest_framework import permissions

class IsOwnerUserProfileOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        else:
            return request.user == obj.user