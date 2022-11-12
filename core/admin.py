from django.contrib import admin

from .models import PriceGroup, Price, GroupFeature, AnalyticRecord, PriceGroupDescription, GroupFeatureSlot, StripeAccount, Token

# Register your models here.
admin.site.register(PriceGroup)
admin.site.register(Price)
admin.site.register(GroupFeature)
admin.site.register(AnalyticRecord)
admin.site.register(PriceGroupDescription)
admin.site.register(GroupFeatureSlot)
admin.site.register(StripeAccount)
admin.site.register(Token)
