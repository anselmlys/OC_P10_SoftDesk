from rest_framework.viewsets import ModelViewSet

from projects.models import Project, Contributor
from projects.serializers import ProjectDetailSerializer, ProjectListSerializer


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def perform_create(self, serializer):
        '''
        During POST, make the authenticated user the author of the project and
        create the Contributor object.
        '''
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(contributors__user=user).distinct()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
