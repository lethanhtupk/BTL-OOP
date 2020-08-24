from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS: 
            # if current request's verb is GET, HEAD or OPTION
            return True
        else: 
            # the method isn't safe method 
            # only author are granted permissions for unsafe method
            return obj.author == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # if current user not admintrators, then return False
            return request.user.is_superuser
        