from rest_framework.viewsets import ModelViewSet

from tracking.serializers import IssueSerializer
from tracking.models import Issue


class IssueViewSet(ModelViewSet):

    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        '''During POST, make the authenticated user the author of the project.'''
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(project__contributors__user=user).distinct()
