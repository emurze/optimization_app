from django.core.validators import MaxValueValidator
from django.db import models

from apps.client.models import Client


class Service(models.Model):
    title = models.CharField(max_length=128, db_index=True)
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ['title']

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
        validators=[
            MaxValueValidator(100)
        ]
    )

    def __str__(self) -> str:
        return self.title


class SubscriptionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .select_related('client', 'service', 'tariff_plan')


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT,
                               related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT,
                                related_name='subscriptions')
    tariff_plan = models.ForeignKey(TariffPlan, models.PROTECT,
                                    related_name='subscriptions')

    objects = SubscriptionManager()

    def __str__(self):
        options = (self.client, self.service, self.tariff_plan)
        return 'client - %s, service - %s, tariff_plan - %s' % options
