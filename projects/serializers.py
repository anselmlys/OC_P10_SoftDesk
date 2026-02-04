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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')

        # Display only projects to which the user is a contributor
        if request and request.user.is_authenticated:
            self.fields['project'].queryset = Project.objects.filter(
                contributors__user=request.user
            ).distinct()

    def validate(self, attrs):
        '''
        Verify that the request user has access to the project.
        '''
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        project = attrs.get('project')
        # For put/patch, keep current project if project is not in request
        if project is None and self.instance is not None:
            project = self.instance.project

        # Check if user is a project contributor
        if project and user and user.is_authenticated:
            is_contributor = Contributor.objects.filter(
                project=project,
                user=user
            ).exists()

            if not is_contributor:
                raise serializers.ValidationError(
                    {'project': 'You are not a contributor of this project.'}
                )

        return attrs


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'created_time', 'updated_at']


class AdminProjectDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    contributors = ContributorListSerializer(many=True, read_only=True)
    issues = IssueListSerializer(many=True, read_only=True)

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
    contributors = ContributorListSerializer(many=True, read_only=True)
    issues = IssueListSerializer(many=True, read_only=True)

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
