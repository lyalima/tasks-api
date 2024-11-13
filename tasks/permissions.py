from rest_framework import permissions


class TaskCreatorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            view.queryset = view.queryset.filter(creator=request.user)
            return True
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
