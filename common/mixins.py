from rest_framework.permissions import IsAuthenticated


from common.permissions import (IsProjectContributor, IsAuthor)


class MultipleSerializerMixin:
    '''
    Return default serializer if action is 'list'.
    Otherwise, return detail serializer.
    '''

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return super().get_serializer_class()
        return self.detail_serializer_class


class ResourcePermissionMixin:
    '''
    Permission is based on action:
    - list/retrieve: contributor
    - create: authenticated
    - update/partial_update/destroy: author
    '''

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsProjectContributor]
        
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthor]
        
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
