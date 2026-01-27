from rest_framework.permissions import BasePermission
from projects.models import Contributor

class IsAdminAuthenticated(BasePermission):
    '''Give access to authenticated admin users.'''
    def has_permission(self, request, view):
        return bool(request.user and
                    request.user.is_authenticated and
                    request.user.is_superuser)


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
        if project is None and obj.__class__.__name__ == "Project":
            project = obj

        # Retrieve the project if obj is a Comment
        if project is None and hasattr(obj, "issue"):
            project = obj.issue.project

        # Do not give access if obj is not Project, Issue or Comment
        if project is None:
            return False

        return Contributor.objects.filter(project=project, user=user).exists()


class IsAuthor(BasePermission):
    '''Give access to the object author (Project/Issue/Comment)'''

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
