from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_15_or_older = models.BooleanField(default=False)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
