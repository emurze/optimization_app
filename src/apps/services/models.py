from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.base.management.commands.createadmin import lg
from apps.client.models import Client
from apps.services.tasks import set_price


class Service(models.Model):
    title = models.CharField(max_length=128, db_index=True)
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ('title',)

    def __str__(self) -> str:
        return self.title


class TariffPlan(models.Model):
    class Types(models.TextChoices):
        FULL = 'FL', 'Full'
        STUDENT = 'SD', 'Student'
        DISCOUNT = 'DC', 'Discount'

    title = models.CharField(max_length=128)
    plan_type = models.CharField(
        max_length=2, default=Types.FULL, choices=Types.choices,
    )
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=(MaxValueValidator(100),)
    )

    def __str__(self) -> str:
        return self.title


@receiver(post_save, sender=TariffPlan)
def set_subscriptions_price(sender, instance, **__) -> None:
    lg.debug(f'Activated post_save signal from {sender.__name__}')
    for subscription in instance.subscriptions.all():
        set_price.delay(subscription.id)


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT,
                               related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT,
                                related_name='subscriptions')
    tariff_plan = models.ForeignKey(TariffPlan, models.PROTECT,
                                    related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)
