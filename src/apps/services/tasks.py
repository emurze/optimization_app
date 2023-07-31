import datetime
import logging
from time import sleep

from celery import shared_task
from celery_singleton import Singleton
from django.core.cache import cache
from django.db import transaction
from django.db.models import F
from django.db.models.functions import Round
from django.conf import settings

lg = logging.getLogger(__name__)


@shared_task(base=Singleton)
def set_price(subscription_id: int) -> None:
    from apps.services.models import Subscription

    with transaction.atomic():
        sleep(1)

        discount = F('tariff_plan__discount_percent')
        price = F('service__price')

        subscription = Subscription.objects\
            .select_for_update()\
            .filter(id=subscription_id)\
            .select_related('service', 'tariff_plan')\
            .annotate(full_price=Round(price * (100 - discount) / 100))\
            .get()

        subscription.price = subscription.full_price
        subscription.save()


@shared_task(base=Singleton)
def set_commit(subscription_id: int) -> None:
    from apps.services.models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects\
            .select_for_update()\
            .filter(id=subscription_id).get()

        subscription.commit = str(datetime.datetime.now())
        subscription.save()

    cache.delete(settings.PRICE_CACHE_NAME)
