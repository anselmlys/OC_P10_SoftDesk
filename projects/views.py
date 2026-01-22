from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from projects.models import Project, Contributor
from projects.serializers import (ProjectDetailSerializer, ProjectListSerializer,
                                  AdminProjectDetailSerializer, ContributorSerializer)
from common.mixins import MultipleSerializerMixin, ResourcePermissionMixin
from common.permissions import (IsAdminAuthenticated, IsProjectContributor,
                                IsAuthor)


class AdminProjectViewset(MultipleSerializerMixin, ModelViewSet):
    
    serializer_class = ProjectListSerializer
    detail_serializer_class = AdminProjectDetailSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ProjectViewset(MultipleSerializerMixin, ResourcePermissionMixin, ModelViewSet):

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


class AdminContributorViewSet(ModelViewSet):

    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ContributorViewSet(ModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def get_queryset(self):
        user = self.request.user
        return Contributor.objects.filter(project__contributors__user=user).distinct()
