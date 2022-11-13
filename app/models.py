from django.db import models
from django.db.models import Sum, Q
import uuid
from numpy.random import choice
from django.contrib.auth.models import User
from django.db.models.constraints import UniqueConstraint
from django.utils import timezone
from .choices import FrontendEvents, ElementTypes
from .utils import default_uuid_string
from core.models import HeatableModel, Token

class Website(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="websites")
    token = models.OneToOneField(Token, on_delete=models.CASCADE, related_name="website", null=True, blank=True)
    dynamic_add_tokens = models.ManyToManyField(Token, related_name="dynamic_website_access", blank=True)
    name = models.CharField(max_length=50, default="", blank=True)
    universal_id = models.UUIDField(default=uuid.uuid4, editable=False)
    url = models.URLField()
    stripe_account_id = models.CharField(max_length=255, default="", blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['owner__email', 'name']

    def __str__(self):
        return f"{self.owner.email} | {self.name}"


    def save(self, *args, **kwargs):
        if self.url.endswith('/'):
            self.url = self.url.rstrip(self.url[-1])

        if not self.token:
            self.token = Token.objects.create(
                user=self.owner
            )
        if not self.name:
            self.name = self.url
            
        super().save(*args, **kwargs)

class ComponentType(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="component_types")
    universal_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['owner__email', 'name']

    def __str__(self):
        return f"{self.owner.email} | {self.name}"

class Component(models.Model):
    universal_id = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=50)
    element_type = models.CharField(max_length=50, choices=ElementTypes.choices, default=ElementTypes.UNKNOWN)
    initial_content = models.TextField(default="")
    xpath = models.TextField(default="", blank=True)
    element_class = models.CharField(max_length=255, default="", blank=True)
    element_id = models.CharField(max_length=255, default="", blank=True)
    type = models.ForeignKey(ComponentType, on_delete=models.CASCADE, related_name="components")
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="components")
    url_path = models.CharField(max_length=255, default="")
    url_query_string = models.CharField(max_length=255, default="")
    css_text = models.TextField(default="", blank=True)
    css_json = models.JSONField(null=True, blank=True)
    selector = models.TextField(default="", blank=True)

    class Meta:
        ordering = ['website__name', 'type__name', 'name']
        constraints = [
            UniqueConstraint(fields=['website', 'xpath'],
                             condition=~Q(xpath=''),
                             name='unique_without_optional'),
        ]

    def __str__(self):
        return f"{self.website.name} | {self.type.name} | {self.name}"

    def save(self, *args, **kwargs):
        result = {}
        if self.css_text:
            property_list = self.css_text.split(';')
            for property in property_list:
                ruleset = property.split(':')

                try:
                    if ruleset[1]:
                        result[ruleset[0]] = ruleset[1] + " !important"
                except:
                    pass

        self.css_json = result

        super().save(*args, **kwargs)

    def get_is_live(self):
        return self.campaigns.filter(end_date=None).exists()

    def get_smart_content(self, cluster=None):
        if False:
            content = cluster.contents.filter(component=self).first()
            if content:
                return content

        contents = self.contents.all().order_by('-hotness')

        if not contents:
            return None

        sum_hotness = contents.aggregate(Sum('hotness'))['hotness__sum']
        normalizer = 1/sum_hotness
         
        weights = [content.hotness * normalizer for content in contents]
        content = choice(list(contents), contents.count(), p=weights)[0]

        return content

    def get_conversions(self):
        return Conversion.objects.filter(contents__component=self).count()

    def get_conversions_value(self):
        sum = Conversion.objects.filter(contents__component=self).aggregate(Sum('conversion_event__value'))['conversion_event__value__sum']
        return sum if sum else 0

class ComponentCampaign(models.Model):
    start_date = models.DateTimeField(auto_now_add=True) 
    end_date = models.DateTimeField(null=True, blank=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="campaigns")

class ComponentConversionEvent(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="conversion_events")
    event = models.CharField(max_length=50, choices=FrontendEvents.choices, default=FrontendEvents.CLICK)
    value = models.FloatField(default=0)

class Content(HeatableModel):
    universal_id = models.UUIDField(default=uuid.uuid4, editable=False)
    text = models.TextField()
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="contents")
    is_suggestion = models.BooleanField(default=False)

    positive_heat_map = {
        FrontendEvents.CLICK: 1,
        FrontendEvents.FOCUS: 1,
        FrontendEvents.HOVER: 1,
    }

    negative_heat_map = {
        FrontendEvents.BLUR: 30,
        FrontendEvents.LEAVE: 15,
    }

    class Meta:
        ordering = ['component__name', '-hotness']

    def __str__(self):
        return f"{self.component.name} | {self.text} | {self.hotness} | {self.get_positive_cluster_count()} | {self.get_negative_cluster_count()}"

    def save(self, *args, **kwargs):
        self.set_confidence(
            self.ups+self.get_positive_cluster_count(), 
            self.downs+self.get_negative_cluster_count()
        )
        if self.confidence == 0:
            self.confidence = 1

        super(Content, self).save(*args, **kwargs)

    def get_hotness_filters(self):
        return {
            'component': self.component
        }

    def get_negative_cluster_count(self):
        return ContentCluster.objects.filter(contents__in=[self]).exclude(analytics__content=self).distinct().count()

    def get_positive_cluster_count(self):
        return ContentCluster.objects.filter(contents__in=[self], analytics__content=self).distinct().count()

    def get_conversions(self):
        return Conversion.objects.filter(contents=self).count()

    def get_clicks(self):
        return Analytic.objects.filter(content=self, event=FrontendEvents.CLICK).count()

    def get_considerations(self):
        return Analytic.objects.filter(content=self).filter(Q(event=FrontendEvents.FOCUS) | Q(event=FrontendEvents.HOVER)).count()

class AnalyticUser(models.Model):
    universal_id = models.CharField(max_length=255, default=default_uuid_string)
    user_ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="users", null=True)

class ContentCluster(models.Model):
    universal_id = models.UUIDField(default=uuid.uuid4, editable=False)
    contents = models.ManyToManyField(Content, related_name="clusters", blank=True)
    analytic_user = models.ForeignKey(AnalyticUser, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.universal_id)

class Analytic(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="analytics")
    event = models.CharField(max_length=50, choices=FrontendEvents.choices, default=FrontendEvents.BLANK)
    content_cluster = models.ForeignKey(ContentCluster, on_delete=models.CASCADE, related_name="analytics", null=True)
    analytic_user = models.ForeignKey(AnalyticUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.content.component.website.name} | {self.content.component.name} | {self.get_event_display()} | {self.created_at}"

class Conversion(models.Model):
    contents = models.ManyToManyField(Content, related_name="conversions")
    content_cluster = models.ForeignKey(ContentCluster, related_name="conversions", on_delete=models.CASCADE)
    conversion_event = models.ForeignKey(ComponentConversionEvent, on_delete=models.CASCADE, related_name="conversions")
    created_at = models.DateTimeField(auto_now_add=True)

