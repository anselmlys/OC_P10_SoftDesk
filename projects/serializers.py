from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'type',
            'author',
            'created_time',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'created_time', 'updated_at']
