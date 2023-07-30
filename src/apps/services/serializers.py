from rest_framework import serializers

from apps.client.models import Client
from apps.services.models import Subscription


class ClientSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Client
        fields = ('full_address', 'client_name', 'email')


class SubscriptionSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    service = serializers.CharField(source='service.title')
    tariff_plan = serializers.CharField(source='tariff_plan.title')
    # price = serializers.CharField(source='service.price')
    # discount = serializers.CharField(source='tariff_plan.discount_percent')
    # clean_price = serializers.SerializerMethodField()
    #
    # @staticmethod
    # def get_clean_price(instance: Subscription) -> int:
    #     discount = instance.tariff_plan.discount_percent
    #     return instance.service.price * (1 - discount // 100)

    class Meta:
        model = Subscription
        fields = (
            'client_id',
            'client',
            'service',
            'tariff_plan',
            'price',
        )
