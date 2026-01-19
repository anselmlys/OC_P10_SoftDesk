from rest_framework import serializers

from tracking.models import Issue


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = [
            'id',
            'name',
            'description',
            'project',
            'status',
            'priority',
            'tag',
            'author',
            'assigned_to',
            'created_time',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'created_time', 'updated_at']
