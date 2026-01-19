from rest_framework import serializers

from tracking.models import Issue


class IssueSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)

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
        ]
        read_only_fields = ['id', 'author', 'created_time', 'updated_at']
