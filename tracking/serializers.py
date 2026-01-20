from rest_framework import serializers

from tracking.models import Issue, Comment


class CommentListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'uuid',
            'created_time',
            'description',
            'author_username',
            'issue'
        ]    


class CommentDetailSerializer(serializers.ModelSerializer):

    issue_name = serializers.CharField(source='issue.name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'uuid',
            'description',
            'issue',
            'issue_name',
            'author',
            'author_username',
            'created_time',
            'updated_at'
        ]
        read_only_fields = ['id', 'uuid', 'author', 'created_time', 'updated_at']


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id',
            'project',
            'name',
            'tag',
            'priority',
            'created_time',
            'updated_at'
        ]


class IssueDetailSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    comments = CommentListSerializer(many=True)

    class Meta:
        model = Issue
        fields = [
            'id',
            'name',
            'description',
            'project',
            'project_name',
            'status',
            'priority',
            'tag',
            'author',
            'author_username',
            'assigned_to',
            'assigned_to_username',
            'created_time',
            'updated_at',
            'comments'
        ]
        read_only_fields = ['id', 'author', 'created_time', 'updated_at']
