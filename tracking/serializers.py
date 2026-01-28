from rest_framework import serializers

from projects.models import Project, Contributor
from tracking.models import Issue, Comment


class CommentListSerializer(serializers.ModelSerializer):
    '''Serializer used to list all comments.'''

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
    '''Serializer used to display the details of a specific comment.'''

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')

        # Display only issues to which the user is a project contributor
        if request and request.user.is_authenticated:
            self.fields['issue'].queryset = Issue.objects.filter(
                project__contributors__user=request.user
            ).distinct()

    def validate(self, attrs):
        '''
        Verify that the request user has access to the project for this issue.
        '''
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        issue = attrs.get('issue')
        # For put/patch, keep current issue if issue is not in request
        if issue is None and self.instance is not None:
            issue = self.instance.issue
        
        # Check if user is a project contributor for this issue
        if issue and user and user.is_authenticated:
            is_contributor = Contributor.objects.filter(
                project=issue.project,
                user=user
            ).exists()

            if not is_contributor:
                raise serializers.ValidationError(
                    {'issue': 'You are not a contributor to this issue\'s project.'}
                )
        
        return attrs


class IssueListSerializer(serializers.ModelSerializer):
    '''Serializer used to list all issues.'''

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
    '''Serializer used to display the details of a specific issue.'''

    project_name = serializers.CharField(source='project.name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)

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
        read_only_fields = ['id', 'author', 'created_time', 'updated_at', 'comments']

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
        Verify that the request user has access to the project and
        that the issue is assigned to a user who is a contributor.
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
                user=user,
            ).exists()

            if not is_contributor:
                raise serializers.ValidationError(
                    {'project': 'You are not a contributor of this project.'}
                )

        assigned_to = attrs.get('assigned_to')
        # Check that the project is assigned to a contributor
        if assigned_to and project:
            assigned_is_contributor = Contributor.objects.filter(
                project=project,
                user=assigned_to,
            ).exists()

            if not assigned_is_contributor:
                raise serializers.ValidationError(
                    {'assigned_to': 'This user is not a contributor of this project.'}
                )
        
        return attrs
