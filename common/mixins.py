class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return super().get_serializer_class()
        return self.detail_serializer_class
