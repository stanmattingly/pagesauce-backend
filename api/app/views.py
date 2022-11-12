import requests

from django.utils import timezone

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import WebsiteSerializer, ComponentSerializer, ComponentTypeSerializer, ContentSerializer, ContentClusterSerializer, AnalyticUserSerializer, AnalyticSerializer
from app.models import Website, Component, ComponentType, AnalyticUser, Analytic, Content, ContentCluster, ComponentConversionEvent, Conversion, ComponentCampaign
from app.choices import FrontendEvents

class WebsiteViewset(ModelViewSet):
    serializer_class = WebsiteSerializer
    queryset = Website.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'universal_id'
    
    def get_queryset(self):
        return Website.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        return Response(WebsiteSerializer(Website.objects.create(
            owner=self.request.user,
            name=request.data.get('name'),
            url=self.request.data.get('url'),
        )).data)

    @action(detail=True, methods=['get'])
    def verify(self, request, universal_id=None):
        website = self.get_object()

        r = requests.get(website.url)

        if f'data-smart-auth-id="{website.token.key}"' in r.text or f"data-smart-auth-id='{website.token.key}'" in r.text:
            website.verified_at = timezone.now()
            website.save()

        return Response(WebsiteSerializer(website).data)

class AnalyticUserViewset(ModelViewSet):
    serializer_class = AnalyticUserSerializer
    queryset = AnalyticUser.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AnalyticUser.objects.filter(website__owner=self.request.user)

    def create(self, request, *args, **kwargs):
        if request.data.get('user_uuid', None):
            user = AnalyticUser.objects.filter(universal_id=request.data.get('user_uuid')).first()
            if user:
                return Response(AnalyticUserSerializer(user).data)
            print(user)
        return Response(AnalyticUserSerializer(AnalyticUser.objects.create(website=request.auth.website)).data)

class AnalyticViewset(ModelViewSet):
    serializer_class = AnalyticSerializer
    queryset = Analytic.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Analytic.objects.filter(analytic_user__website__owner=self.request.user)

    def create(self, request, *args, **kwargs):
        content_uuid = request.data.get('content_uuid')
        component_uuid = request.data.get('component_uuid')
        content = None

        component = Component.objects.get(universal_id=component_uuid)

        try:
            content = Content.objects.get(universal_id=content_uuid)
        except:
            if not component.contents.exists():
                content = Content.objects.create(
                    text=component.name,
                    component=component
                )
            else:
                return Response({})

        analytic_user = AnalyticUser.objects.get(universal_id=request.data.get('user_uuid'))
        
        try:
            cluster = ContentCluster.objects.get(universal_id=request.data.get('cluster_uuid'))
        except ContentCluster.DoesNotExist:
            cluster = ContentCluster.objects.create(analytic_user=analytic_user)
            cluster.contents.add(content)

        event = request.data.get('event', FrontendEvents.BLANK)
        conversion_event = ComponentConversionEvent.objects.filter(component=content.component, event=event).first()

        analytic = Analytic.objects.create(content=content, analytic_user=analytic_user, event=event, content_cluster=cluster)

        if conversion_event:
            conversion = Conversion.objects.create(content_cluster=cluster, conversion_event=conversion_event)
            conversion.contents.add(*cluster.contents.all())

        if event in content.positive_heat_map:
            content.ups += content.positive_heat_map[event]

        if event in content.negative_heat_map:
            content.downs += content.negative_heat_map[event]

        if conversion_event:
            content.ups += 5
            for related_content in cluster.contents.exclude(pk=content.pk):
                related_content.ups += 5
                related_content.save()

        content.save()

        return Response(AnalyticSerializer(analytic).data)

class ContentClusterViewset(ModelViewSet):
    serializer_class = ContentClusterSerializer
    queryset = ContentCluster.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'universal_id'
    
    def get_queryset(self):
        return ContentCluster.objects.filter(analytic_user__website=self.request.auth.website)

    def create(self, request, *args, **kwargs):
        contents = Content.objects.filter(universal_id__in=request.data.get('contents', []))
        try:
            analytic_user = AnalyticUser.objects.get(universal_id=request.data.get('user_uuid'))
        except AnalyticUser.DoesNotExist:
            analytic_user = AnalyticUser.objects.create(website=request.auth.website)
        url = request.data.get('url')
        
        cluster = ContentCluster.objects.create(analytic_user=analytic_user, url=url)

        if contents:
            cluster.contents.add(*contents)

        return Response(ContentClusterSerializer(cluster).data)

    def partial_update(self, request, universal_id=None):
        cluster = self.get_object()
        contents = Content.objects.filter(universal_id__in=request.data.get('contents', []))

        if contents:
            cluster.contents.add(*contents)

        return Response(ContentClusterSerializer(cluster).data)

    @action(detail=True, methods=['post'])
    def add_contents(self, request, universal_id=None):
        cluster = self.get_object()
        contents = Content.objects.filter(universal_id__in=request.data.get('contents', []))

        if contents:
            cluster.contents.add(*contents)

        return Response(ContentClusterSerializer(cluster).data)


class ComponentViewset(ModelViewSet):
    serializer_class = ComponentSerializer
    queryset = Component.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'universal_id'
    
    def get_queryset(self):
        try:
            return self.request.auth.website.components.all()
        except:
            website_uuid = self.request.query_params.get('website_uuid', None)
            queryset = Component.objects.filter(website__owner=self.request.user)

            if website_uuid:
                queryset = queryset.filter(website__universal_id=website_uuid)

            return queryset

    @action(detail=False, methods=['post'])
    def set_live_status(self, request):
        component = Component.objects.get(universal_id=request.data.get('component_uuid'))
        status = request.data.get('status')

        if status == False:
            current_campaign = component.campaigns.filter(end_date=None).first()
            current_campaign.end_date = timezone.now()
            current_campaign.save()

        if status == True:
            ComponentCampaign.objects.create(component=component)

        return Response(ComponentSerializer(component).data)

    @action(detail=True, methods=['post'])
    def create_conversion(self, request, universal_id=None):
        component = self.get_object()
        event = request.data.get('event')
        value = request.data.get('value')

        ComponentConversionEvent.objects.create(
            component=component,
            event=event,
            value=value
        )

        return Response({})

    @action(detail=False, methods=['get'])
    def get_smart_content(self, request):
        id = request.query_params.get('id')
        cluster_uuid = request.query_params.get('cluster_uuid')
        cluster = ContentCluster.objects.filter(universal_id=cluster_uuid).first()

        try:
            component = Component.objects.get(universal_id=id)
        except:
            component = Component.objects.get(xpath=id)

        content = component.get_smart_content(cluster)

        serializer = ContentSerializer(content)

        Analytic.objects.create(
            content=content,
            event=FrontendEvents.VIEW,
            content_cluster=cluster,
            analytic_user=cluster.analytic_user,
        )

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_xpath_components(self, request):
        queryset = self.get_queryset().filter(pk__in=ComponentCampaign.objects.filter(component__website=request.auth.website, end_date=None).values('component__pk'))
        serializer = ComponentSerializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if hasattr(request, 'auth'):
            website = request.auth.website
            user = website.owner
            component_type, _ = ComponentType.objects.get_or_create(owner=user, name="Click to Add")
            name = request.data.get('name')
            xpath = request.data.get('xpath')
            selector = request.data.get('selector', '')
            element_class = request.data.get('element_class', '')
            element_id = request.data.get('element_id', '')
            element_type = request.data.get('element_type', '')
            initial_content = request.data.get('initial_content', '')
            url_path = request.data.get('url_path', '')
            url_query_string = request.data.get('url_query_string', '')
            css_json = request.data.get('css_json', {})
            css_text = request.data.get('css_text', {})

            component, _ = Component.objects.get_or_create(
                website=website, 
                type=component_type, 
                xpath=xpath,
                selector=selector,
            )

            component.name = name
            component.element_type = element_type
            component.initial_content = initial_content
            component.element_class = element_class
            component.element_id = element_id
            component.url_path = url_path
            component.url_query_string = url_query_string
            component.css_json = css_json
            component.css_text = css_text

            component.save()

            Content.objects.get_or_create(text=initial_content, component=component)

            return Response(ComponentSerializer(component).data)
        else:
            component_type = ComponentType.objects.get(universal_id=request.data.get('type_uuid'))
            website = Website.objects.get(universal_id=request.data.get('website_uuid'))
            name = request.data.get('name')

            return Response(ComponentSerializer(Component.objects.create(website=website, name=name, type=component_type)).data)


class ComponentTypeViewset(ModelViewSet):
    serializer_class = ComponentTypeSerializer
    queryset = ComponentType.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'universal_id'
    
    def get_queryset(self):
        return ComponentType.objects.filter(owner=self.request.user)

class ContentViewset(ModelViewSet):
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'universal_id'
    
    def get_queryset(self):
        queryset = Content.objects.filter(component__type__owner=self.request.user)
        component_uuid = self.request.query_params.get('component_uuid')

        if component_uuid:
            queryset = queryset.filter(component__universal_id=component_uuid)

        return queryset

    def create(self, request, *args, **kwargs):
        component = Component.objects.get(universal_id=request.data.get('component_uuid'))
        text = request.data.get('text')

        return Response(ContentSerializer(Content.objects.create(component=component, text=text)).data)

