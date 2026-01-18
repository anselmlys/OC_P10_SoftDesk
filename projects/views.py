from rest_framework.viewsets import ModelViewSet

from projects.models import Project, Contributor
from projects.serializers import ProjectSerializer


class ProjectViewset(ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        '''
        During POST, make the authenticated user the author of the project and
        create the Contributor object.
        '''
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)
