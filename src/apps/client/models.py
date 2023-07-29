from typing import cast

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ClientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user')


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, db_index=True)
    company_name = models.CharField(max_length=128)
    full_address = models.CharField(max_length=128)

    objects = ClientManager()

    def __str__(self):
        user = cast(User, self.user)
        return user.username
