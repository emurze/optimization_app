from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.client.models import User
from apps.services.models import Subscription
from apps.services.serializers import SubscriptionSerializer


class SubscriptionViewSet(ReadOnlyModelViewSet):
    queryset = Subscription.objects\
        .prefetch_related(
            Prefetch('client__user',
                     queryset=User.objects.only('username', 'email'))
        )\
        .only('client_id', 'client__user_id', 'client__full_address',
              'service__title', 'tariff_plan__title')
    serializer_class = SubscriptionSerializer
