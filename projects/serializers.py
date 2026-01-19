from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

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
        ]
        read_only_fields = ['id', 'author', 'created_time', 'updated_at']
