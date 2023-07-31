from django.core.cache import cache
from django.db.models import Prefetch, Sum
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.client.models import User
from apps.services.models import Subscription
from apps.services.serializers import SubscriptionSerializer
from django.conf import settings


class SubscriptionViewSet(ReadOnlyModelViewSet):
    queryset = Subscription.objects\
        .select_related('service', 'tariff_plan', 'client')\
        .prefetch_related(
            Prefetch('client__user',
                     queryset=User.objects.only('username', 'email'))
        )\
        .only('client_id', 'client__user_id', 'client__full_address',
              'service__title', 'service__price', 'price',
              'tariff_plan__title', 'tariff_plan__discount_percent',)\

    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        response = super().list(request, *args, **kwargs)

        if price_cache := cache.get(settings.PRICE_CACHE_NAME):
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60)

        new_response = {
            'result': response.data,
            'total_amount': total_price,
        }
        return Response(new_response)

