"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import AnalyticsUserViewset, PriceGroupDescriptionViewSet, PriceGroupViewSet, PriceViewSet, GroupFeatureViewSet, AnalyticRecordViewSet, StripeAccountViewSet, UserViewSet
from api.auth.views import LoginViewSet, RegistrationViewSet, RefreshViewSet, VerifySmartAddTokenViewset
from api.app.views import WebsiteViewset, ComponentViewset, ComponentTypeViewset, AnalyticUserViewset, AnalyticViewset, ContentClusterViewset, ContentViewset
from api.documentation.views import DocumentationView
from core.views import RenderWidgetView, WebhookView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'price-groups', PriceGroupViewSet)
router.register(r'prices', PriceViewSet)
router.register(r'features', GroupFeatureViewSet)
router.register(r'analytic-records', AnalyticRecordViewSet)
router.register(r'price-group-descriptions', PriceGroupDescriptionViewSet)
router.register(r'analytics-users', AnalyticsUserViewset)
router.register(r'stripe-accounts', StripeAccountViewSet)
router.register(r'users', UserViewSet)

# Auth
auth_router = routers.DefaultRouter()
auth_router.register(r'register', RegistrationViewSet)
auth_router.register(r'login', LoginViewSet)
auth_router.register(r'refresh', RefreshViewSet)
auth_router.register(r'smart-add-tokens', VerifySmartAddTokenViewset)

# App
app_router = routers.DefaultRouter()
app_router.register(r'websites', WebsiteViewset)
app_router.register(r'components', ComponentViewset)
app_router.register(r'component-types', ComponentTypeViewset)
app_router.register(r'analytic-users', AnalyticUserViewset)
app_router.register(r'analytics', AnalyticViewset)
app_router.register(r'content-clusters', ContentClusterViewset)
app_router.register(r'contents', ContentViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path('api/', include(router.urls)),
    path('auth/', include(auth_router.urls)),
    path('api/app/', include(app_router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('smart-price/documentation/', DocumentationView.as_view(), name="documentation"),
    path('widget/', RenderWidgetView.as_view(), name="widget"),
    path('webhooks/', WebhookView.as_view(), name="webhooks"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
