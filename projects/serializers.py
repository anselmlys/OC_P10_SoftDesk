from rest_framework import serializers

from projects.models import Project, Contributor
from tracking.serializers import IssueListSerializer


class ContributorListSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Contributor
        fields = [
            'user',
            'user_username'
        ]


class ContributorSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'user_username',
            'project',
            'project_name'
        ]


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'created_time', 'updated_at']


class AdminProjectDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    contributors = ContributorListSerializer(many=True)
    issues = IssueListSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'type',
            'author',
            'author_username',
            'created_time',
            'updated_at',
            'contributors',
            'issues',
        ]
        read_only_fields = ['id', 'created_time', 'updated_at', 'issues']
    
    def get_contributors_usernames(self, obj):
        return [c.user.username for c in obj.contributors.all()]


class ProjectDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    contributors = ContributorListSerializer(many=True)
    issues = IssueListSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'type',
            'author',
            'author_username',
            'created_time',
            'updated_at',
            'contributors',
            'issues',
        ]
        read_only_fields = ['id', 'author', 'created_time', 'updated_at', 'issues']

    def get_contributors_usernames(self, obj):
        return [c.user.username for c in obj.contributors.all()]
