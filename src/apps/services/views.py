from django.db.models import Prefetch, F, Sum
from rest_framework.response import Response
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
              'service__title', 'service__price', 'price',
              'tariff_plan__title', 'tariff_plan__discount_percent',)\
        # .annotate(
        #     price=(
        #         F('service__price') *
        #         (100 - F('tariff_plan__discount_percent'))
        #     )
        # )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        response = super().list(request, *args, **kwargs)
        total_amount = queryset.aggregate(total=Sum('price')).get('total')
        new_response = {
            'result': response.data,
            'total_amount': total_amount,
        }
        return Response(new_response)

