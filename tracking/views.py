from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from tracking.serializers import (IssueListSerializer, IssueDetailSerializer,
                                  CommentListSerializer, CommentDetailSerializer)
from tracking.models import Issue, Comment
from common.mixins import MultipleSerializerMixin, ResourcePermissionMixin
from common.permissions import IsAdminAuthenticated


class AdminIssueViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    queryset = Issue.objects.all()
    permission_classes = [IsAdminAuthenticated]


class IssueViewSet(MultipleSerializerMixin, ResourcePermissionMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def perform_create(self, serializer):
        '''During POST, make the authenticated user the author of the project.'''
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(project__contributors__user=user).distinct()


class AdminCommentViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAdminAuthenticated]


class CommentViewSet(MultipleSerializerMixin, ResourcePermissionMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(issue__project__contributors__user=user).distinct()
