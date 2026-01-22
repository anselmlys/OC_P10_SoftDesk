from rest_framework.permissions import BasePermission
from projects.models import Contributor

class IsAdminAuthenticated(BasePermission):
    '''Give access to authenticated admin users.'''
    def has_permission(self, request, view):
        return bool(request.user and
                    request.user.is_authenticated and
                    request.user.is_superuser)


class IsProjectContributor(BasePermission):
    '''Give access to project contributor.'''
    
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(project=obj, user=request.user).exists()


class IsAuthor(BasePermission):
    '''Give access to the object author (Project/Issue/Comment)'''

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
