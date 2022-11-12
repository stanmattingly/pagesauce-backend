import uuid

from core import stripe as stripe_utils

from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.contrib.auth.models import User

from .serializers import AnalyticsUserSerializer, AnalyticRecordSerializer, PriceGroupSerializer, PriceSerializer, GroupFeatureSerializer, PriceGroupDesciptionSerializer, StripeAccountSerializer, UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from core.models import (
    AnalyticsUser, 
    GroupFeatureSlot, 
    PriceGroup, 
    Price, 
    GroupFeature, 
    AnalyticRecord, 
    Actions, 
    PriceGroupDescription,
    StripeAccount
)


class UserViewSet(viewsets.ModelViewSet):
    """
    Get, List and Create Price Groups
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all().prefetch_related('stripe_accounts')


    @action(detail=False)
    def get_current_user(self, request):
        return Response(UserSerializer(request.user).data)


class StripeAccountViewSet(viewsets.ModelViewSet):
    """
    Get, List and Create Price Groups
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StripeAccountSerializer
    queryset = StripeAccount.objects.all()

    def create(self, request, format='json'):
        auth_code = request.data.get('auth_code')
        stripe_account = StripeAccount.objects.filter(code=auth_code).first()

        if not stripe_account:
            try:
                account_id = stripe_utils.get_account_id_from_code(auth_code)
                stripe_account = StripeAccount.objects.create(
                    user=request.user,
                    account_id=account_id,
                    business_name=stripe_utils.get_stripe_business_name(account_id),
                    code=auth_code
                )
                stripe_utils.sync_stripe_account(stripe_account)

            except Exception as e:
                return Response({})

        return Response(StripeAccountSerializer(stripe_account).data)
        


class PriceGroupViewSet(viewsets.ModelViewSet):
    """
    Get, List and Create Price Groups
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PriceGroupSerializer
    queryset = PriceGroup.objects.all()

    def get_queryset(self):
        account_id = self.request.GET.get("account_id", "")
        hottest_prices = self.request.GET.get("hottest_prices", False)

        price_queryset = Price.objects.all()

        if hottest_prices:
            price_queryset = price_queryset.order_by('-hotness')
        
        return PriceGroup.objects.filter(stripe_account__account_id=account_id).prefetch_related(Prefetch('prices', queryset=price_queryset), 'slots', 'group_analytics')


class PriceGroupDescriptionViewSet(viewsets.ModelViewSet):
    """
    Get, List and Create Price Group Descriptions
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PriceGroupDesciptionSerializer
    queryset = PriceGroupDescription.objects.all().order_by('group', '-hotness')

    def get_queryset(self):
        group_name = self.request.GET.get('group_name')

        return PriceGroupDescription.objects.filter(group__name=group_name).order_by('-hotness') if group_name else PriceGroupDescription.objects.all().order_by('group', '-hotness')


    @action(detail=False)
    def get_group_description(self, request):
        group_id = request.GET.get('group_id')
        user_id = request.GET.get('user_id')

        group = get_object_or_404(PriceGroup, pk=group_id)
        user = get_object_or_404(AnalyticsUser, pk=user_id)
        description = PriceGroupDescription.objects.filter(group=group, users__in=[user]).first()

        if description:
            serializer = PriceGroupDesciptionSerializer(description, context={"request": request})
            return Response(serializer.data)

        else:
            description = group.get_smart_description()
            if description:
                description.users.add(user)
            serializer = PriceGroupDesciptionSerializer(description, context={"request": request})
            return Response(serializer.data)


class PriceViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving PriceGroup objects.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PriceSerializer
    queryset = Price.objects.all().order_by('group', '-hotness')

    def get_queryset(self):
        group_name = self.request.GET.get('group_name')

        return Price.objects.filter(group__name=group_name).order_by('-hotness') if group_name else Price.objects.all().order_by('group', '-hotness')

    def list(self, request):
        response = super().list(request)

        return response


    @action(detail=False)
    def get_group_price(self, request):
        group_id = request.GET.get('group_id')
        user_id = request.GET.get('user_id')

        group = get_object_or_404(PriceGroup, pk=group_id)
        user = get_object_or_404(AnalyticsUser, pk=user_id)
        price = Price.objects.filter(group=group, users__in=[user]).first()

        if price:
            serializer = PriceSerializer(price, context={"request": request})
            return Response(serializer.data)

        else:
            price = group.get_smart_price()
            price.users.add(user)
            serializer = PriceSerializer(price, context={"request": request})
            return Response(serializer.data)


class GroupFeatureViewSet(viewsets.ModelViewSet):
    """
    Get, List and Create Price Group Features
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GroupFeatureSerializer
    queryset = GroupFeature.objects.all()

    def get_queryset(self):
        group_name = self.request.GET.get('group_name')

        return GroupFeature.objects.filter(slot__group__name=group_name).order_by('slot__order', '-hotness') if group_name else GroupFeature.objects.all().order_by('slot__group', '-hotness') 

    @action(detail=False)
    def get_group_features(self, request):
        group_id = request.GET.get('group_id')
        user_id = request.GET.get('user_id')

        group = get_object_or_404(PriceGroup, pk=group_id)
        user = get_object_or_404(AnalyticsUser, pk=uuid.UUID(user_id))
        features = GroupFeature.objects.filter(slot__group=group, users__in=[user])

        if features:
            serializer = GroupFeatureSerializer(features, context={"request": request}, many=True)
            return Response(serializer.data)

        else:
            features = []
            for slot in GroupFeatureSlot.objects.filter(group=group):
                feature = slot.get_smart_feature()
                feature.users.add(user)
                features.append(feature)

            serializer = GroupFeatureSerializer(features, context={"request": request}, many=True)
            return Response(serializer.data)


    
class AnalyticRecordViewSet(viewsets.ModelViewSet):
    """
    Get, List and Create Analytics Records
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AnalyticRecordSerializer
    queryset = AnalyticRecord.objects.all()

    def get_queryset(self):
        account_id = self.request.GET.get('account_id', "")
        return AnalyticRecord.objects.filter(group__stripe_account__account_id=account_id).order_by("-created_at").prefetch_related("group", "price", "group_description", "features")

    def create(self, request, format='json'):
        user_id = request.data.get('user_id')
        group_id = request.data.get('group_id')
        action_string = request.data.get('action_string')

        user = get_object_or_404(AnalyticsUser, pk=uuid.UUID(user_id))
        group = get_object_or_404(PriceGroup, pk=group_id)

        new_analytic = AnalyticRecord.objects.create(
            action=action_string,
            user=user,
            group=group,
            price=group.get_price_by_user(user),
            group_description=group.get_description_by_user(user),
        )
        new_analytic.features.add(*group.get_features_by_user(user))

        ups_increment = 0
        downs_increment = 0

        if action_string == Actions.HOVER:
            ups_increment = 1
        elif action_string == Actions.LEAVE:
            downs_increment = .5
        elif action_string == Actions.SELECT:
            ups_increment = 10
        elif action_string == Actions.UNSELECT:
            downs_increment = 5
        elif action_string == Actions.SIGNUP_HOVER:
            ups_increment = 50
        elif action_string == Actions.SIGNUP_LEAVE:
            downs_increment = 25
        elif action_string == Actions.SIGNUP_CLICK:
            ups_increment = 100
        elif action_string == Actions.VIEW:
            ups_increment = 0
        elif action_string == Actions.CONVERSION_CLICK:
            ups_increment = 1000
        elif action_string == Actions.CONVERSION_HOVER:
            ups_increment = 30
        elif action_string == Actions.CONVERSION_LEAVE:
            downs_increment = 15
        else:
            ups_increment = 0

        new_analytic.group.ups += ups_increment
        new_analytic.group.downs += downs_increment
        new_analytic.price.ups += ups_increment
        new_analytic.price.downs += downs_increment

        new_analytic.group.save()
        new_analytic.price.save()

        if new_analytic.group_description:
            new_analytic.group_description.ups += ups_increment
            new_analytic.group_description.downs += downs_increment
            new_analytic.group_description.save()

        for feature in new_analytic.features.all():
            feature.ups += ups_increment
            feature.downs += downs_increment
            feature.save()

        serializer = AnalyticRecordSerializer(new_analytic, context={"request": request})

        return Response(serializer.data)


class AnalyticsUserViewset(viewsets.ModelViewSet):
    """
    Get, List and Analytics Users
    """

    serializer_class = AnalyticsUserSerializer
    queryset = AnalyticsUser.objects.all()

    def create(self, request, format="json"):
        user_id = request.data.get("user_id")

        try:
            user = AnalyticsUser.objects.filter(pk=uuid.UUID(user_id)).first()
        except:
            user = None

        if user:
            return Response(AnalyticsUserSerializer(user).data)
        else:
            return Response(AnalyticsUserSerializer(AnalyticsUser.objects.create()).data)



