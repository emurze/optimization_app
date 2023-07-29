from django.urls import path, include
from rest_framework import routers

from apps.services.views import SubscriptionViewSet

app_name = 'services'

router = routers.DefaultRouter()
router.register(r'api/subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
