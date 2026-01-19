from rest_framework.viewsets import ModelViewSet

from tracking.serializers import IssueSerializer
from tracking.models import Issue


class IssueViewSet(ModelViewSet):

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        '''During POST, make the authenticated user the author of the project.'''
        serializer.save(author=self.request.user)
