from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .serializers import LoginSerializer, RegisterSerializer, TokenSerializer

from django.contrib.auth.models import User
from django.utils import timezone
from app.models import Website, ComponentType
from app.initial_component_types import INITIAL_COMPONENT_TYPES
from core.models import Token


class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        url = data.pop("website")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        
        website = Website.objects.create(
            owner=user,
            name=url,
            url=url
        )

        for component_type in INITIAL_COMPONENT_TYPES:
            ComponentType.objects.create(
                owner=user,
                name = component_type,
            )

        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "website": website.universal_id,
        }

        return Response({
            "user": serializer.data,
            "refresh": res["refresh"],
            "access": res["access"],
            "website": website.universal_id,
        }, status=status.HTTP_201_CREATED)


class RefreshViewSet(ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class VerifySmartAddTokenViewset(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post']
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'key'

    def get_queryset(self):
        return Token.objects.filter(dynamic_website_access__in=[self.request.auth.website], expiry__gte=timezone.now())

    def create(self, request, *args, **kwargs):
        website_uuid = request.data.get('website_uuid')
        user = request.user

        website = Website.objects.filter(universal_id=website_uuid, owner=user).first()

        if website:
            token = Token.objects.filter(user=user, expiry__gte=timezone.now(), dynamic_website_access__in=[website]).first()

            if not token:
                token = Token.objects.create(
                    user=user,
                    expiry=timezone.now() + timezone.timedelta(hours=1)
                )
                website.dynamic_add_tokens.add(token)

            url_build = f"{website.url}/?smart-add-token={token.key}"

            data = TokenSerializer(token).data
            data['url_build'] = url_build

            return Response(data)

        else:
            return Response({})

