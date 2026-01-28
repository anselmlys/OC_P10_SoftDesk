from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from projects.models import Contributor

class IsAdminAuthenticated(BasePermission):
    '''Give access to authenticated admin users.'''
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated(detail="Authentication credentials were not provided.")
        
        if not request.user.is_superuser:
            raise PermissionDenied(detail='Admin access required.')

        return True


class IsProjectContributor(BasePermission):
    '''
    Give access to project contributor.
    Can only give acess to objects which are either Project, Issue or Comment.
    '''
    
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Retrieve the project if obj is an Issue
        project = getattr(obj, 'project', None)

        # Check if obj is the project
        if project is None and obj.__class__.__name__ == 'Project':
            project = obj

        # Retrieve the project if obj is a Comment
        if project is None and hasattr(obj, 'issue'):
            project = obj.issue.project

        # Do not give access if obj is not Project, Issue or Comment
        if project is None:
            raise PermissionDenied(detail='Access denied.')
        
        # Check if user is a contributor of the project
        is_contributor = Contributor.objects.filter(project=project, user=user).exists()
        if not is_contributor:
            raise PermissionDenied(detail='You must be a contributor of this project.')

        return True


class IsAuthor(BasePermission):
    '''Give access to the object author (Project/Issue/Comment)'''

    def has_object_permission(self, request, view, obj):
        if obj.author != request.user:
            raise PermissionDenied(detail='You must be the author of this resource.')

        return True
