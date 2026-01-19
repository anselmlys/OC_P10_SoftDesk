from django.contrib import admin

from tracking.models import Issue, Comment


admin.site.register(Issue)
admin.site.register(Comment)
