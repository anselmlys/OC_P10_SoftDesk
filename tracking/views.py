from rest_framework.viewsets import ModelViewSet

from tracking.serializers import IssueListSerializer, IssueDetailSerializer
from tracking.models import Issue


class IssueViewSet(ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def perform_create(self, serializer):
        '''During POST, make the authenticated user the author of the project.'''
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(project__contributors__user=user).distinct()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return super().get_serializer_class()
        return self.detail_serializer_class
