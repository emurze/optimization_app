from django.contrib import admin

from apps.services.models import TariffPlan, Service, Subscription

admin.site.register(Service)
admin.site.register(TariffPlan)
admin.site.register(Subscription)
