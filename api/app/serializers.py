from tokenize import Token
from app.models import (
    Website,
    ComponentType,
    Component,
    Content,
    ContentCluster,
    AnalyticUser,
    Analytic,
    ComponentConversionEvent
)
from ..auth.serializers import TokenSerializer
from app.choices import FrontendEvents
from rest_framework import serializers



class WebsiteSerializer(serializers.ModelSerializer):
    token = TokenSerializer()
    
    class Meta:
        model = Website
        fields = '__all__'

class ComponentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentType
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    normalized_hotness = serializers.SerializerMethodField()
    conversions = serializers.IntegerField(source='get_conversions')
    clicks = serializers.IntegerField(source='get_clicks')
    considerations = serializers.IntegerField(source='get_considerations')

    class Meta:
        model = Content
        fields = '__all__'

    def get_normalized_hotness(self, obj):
        return obj.get_normalized_hotness()

    def get_conversions(self, obj):
        return obj.get_conversions()

class ComponentConversionEventSerializer(serializers.ModelSerializer):
    event = serializers.CharField(source='get_event_display')
    class Meta:
        model = ComponentConversionEvent
        fields = '__all__'

class ComponentSerializer(serializers.ModelSerializer):
    type = ComponentTypeSerializer()
    element_type = serializers.CharField(source='get_element_type_display')
    hottest_content = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    conversions = serializers.IntegerField(source='get_conversions')
    conversions_value = serializers.IntegerField(source='get_conversions_value')
    clicks = serializers.SerializerMethodField()
    website = WebsiteSerializer()
    is_live = serializers.BooleanField(source='get_is_live')
    conversion_events = ComponentConversionEventSerializer(many=True)

    class Meta:
        model = Component
        fields = '__all__'

    def get_hottest_content(self, obj):
        return ContentSerializer(obj.contents.order_by('-hotness').first()).data

    def get_views(self, obj):
        return ContentCluster.objects.filter(contents__component__in=[obj]).distinct().count()

    def get_conversions(self, obj):
        return obj.get_conversions()

    def get_clicks(self, obj):
        return Analytic.objects.filter(content__component=obj, event=FrontendEvents.CLICK).count()

class AnalyticUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticUser
        fields = '__all__'

class ContentClusterSerializer(serializers.ModelSerializer):
    analytic_user = AnalyticUserSerializer()
    
    class Meta:
        model = ContentCluster
        fields = '__all__'

class AnalyticSerializer(serializers.ModelSerializer):
    content_cluster = ContentClusterSerializer()
    content = ContentSerializer()
    component_name = serializers.SerializerMethodField()
    event = serializers.CharField(source='get_event_display')

    class Meta:
        model = Analytic
        fields = '__all__'

    def get_component_name(self, obj):
        return obj.content.component.name