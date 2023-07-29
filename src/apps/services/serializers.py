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

    # client_name = serializers.CharField(source='client.user.username')
    # client_address = serializers.CharField(source='client.full_address')
    # email = serializers.CharField(source='client.user.email')
    client = ClientSerializer(many=False)

    service = serializers.CharField(source='service.title')
    tariff_plan = serializers.CharField(source='tariff_plan.title')

    class Meta:
        model = Subscription
        fields = (
            'client_id',
            'client',
            # 'client_address', 
            # 'client_name', 
            # 'email',
            'service',
            'tariff_plan',
        )
