import logging

from celery import shared_task
from django.db.models import Subquery, OuterRef, F
from django.db.models.functions import Round

lg = logging.getLogger(__name__)


@shared_task
def set_price(subscription_id) -> None:
    from apps.services.models import Subscription

    discount = F('tariff_plan__discount_percent')
    price = F('service__price')

    subscription = Subscription.objects.filter(id=subscription_id)\
        .select_related('service', 'tariff_plan')\
        .annotate(full_price=Round((price * (1 - discount / 100))))\
        .update()

    subscription.price = subscription.full_price
    subscription.save()
