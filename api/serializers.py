from core.models import (
    AnalyticsUser, 
    PriceGroup, 
    GroupFeature, 
    Price, 
    AnalyticRecord, 
    GroupFeatureSlot,
    PriceGroupDescription,
    StripeAccount,
)
from core.choices import Actions
from rest_framework import serializers
from django.db.models import Sum
from django.contrib.auth.models import User



class AnalyticsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsUser
        fields = '__all__'

class StripeAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeAccount
        fields = ['account_id', 'code', 'business_name']

class UserSerializer(serializers.ModelSerializer):
    stripe_accounts = StripeAccountSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'stripe_accounts']
        read_only_fields = ['stripe_accounts']


class GroupFeatureSlotSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = GroupFeatureSlot
        fields = '__all__'

class GroupFeatureSerializer(serializers.ModelSerializer):
    slot = GroupFeatureSlotSerializer()
    class Meta:
        model = GroupFeature
        fields = '__all__'


class PriceGroupDesciptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    
    class Meta:
        model = PriceGroupDescription
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    normalized_hotness = serializers.SerializerMethodField()
    interaction_count = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields = '__all__'

    def get_interaction_count(self, obj):
        return obj.price_analytics.filter(action=Actions.CONVERSION_CLICK).count()

    def get_normalized_hotness(self, obj):
        return round((1 / Price.objects.filter(group=obj.group).aggregate(Sum('hotness'))['hotness__sum']) * obj.hotness * 100, 4)

class PriceGroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    slots = GroupFeatureSlotSerializer(many=True)
    prices = PriceSerializer(many=True)
    
    class Meta:
        model = PriceGroup
        fields = '__all__'

class AnalyticRecordSerializer(serializers.ModelSerializer):
    group = PriceGroupSerializer() 
    price = PriceSerializer()
    group_description = PriceGroupDesciptionSerializer()
    features = GroupFeatureSerializer(many=True)
    action = serializers.CharField(source='get_action_display')

    class Meta:
        model = AnalyticRecord
        fields = '__all__'