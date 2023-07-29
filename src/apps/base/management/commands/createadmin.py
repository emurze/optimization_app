import logging
import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

DEFAULT_ADMIN_NAME = 'adm1'
DEFAULT_ADMIN_PASSWORD = 'adm1'
DEFAULT_ADMIN_EMAIL = 'adm1@adm1.com'

User = get_user_model()
lg = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This command create superuser'

    def handle(self, *_, **__) -> None:
        if not User.objects.exists():
            user = User.objects.create_superuser(
                username=os.getenv('ADMIN_NAME', DEFAULT_ADMIN_NAME),
                email=os.getenv('ADMIN_EMAIL', DEFAULT_ADMIN_EMAIL),
                password=os.getenv('ADMIN_PASSWORD', DEFAULT_ADMIN_PASSWORD),
            )
            lg.debug(f'Admin {user.username} was created.')
