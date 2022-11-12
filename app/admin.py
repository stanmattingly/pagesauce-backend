from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Website, ComponentType, Component, Content, Analytic, AnalyticUser, ContentCluster, ComponentConversionEvent, Conversion, ComponentCampaign

# Register your models here.
admin.site.register(Website)
admin.site.register(ComponentType)
admin.site.register(Component)
admin.site.register(Content)
admin.site.register(Analytic)
admin.site.register(AnalyticUser)
admin.site.register(ContentCluster)
admin.site.register(ComponentConversionEvent)
admin.site.register(Conversion)
admin.site.register(ComponentCampaign)