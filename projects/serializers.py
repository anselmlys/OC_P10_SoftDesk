from rest_framework import serializers

from projects.models import Project
from tracking.serializers import IssueListSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'created_time', 'updated_at']


class ProjectDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    contributors_usernames = serializers.SerializerMethodField()

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
            'contributors_usernames',
            'issues',
        ]
        read_only_fields = ['id', 'author', 'created_time', 'updated_at', 'issues']

    def get_contributors_usernames(self, obj):
        return [c.user.username for c in obj.contributors.all()]
