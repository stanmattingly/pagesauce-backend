import uuid
from numpy.random import choice
from django.db import models
from django.db.models import Min, Max
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token as RestToken

from .choices import Actions, Terms
from .hotness import get_temp, get_confidence


class Token(RestToken):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    expiry = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class HeatableModel(models.Model):
    hotness = models.FloatField(default=0)
    confidence = models.FloatField(default=1)
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.set_hotness()
        super(HeatableModel, self).save(*args, **kwargs)

    def set_hotness(self):
        self.hotness = get_temp(self.ups, self.downs, self.created_at)

    def set_confidence(self, ups, downs):
        self.confidence = get_confidence(ups, downs)

    def reset_hotness(self):
        self.ups = 0
        self.downs = 0
        self.confidence = 0
        self.created_at = timezone.now()
        self.save()

    def get_hotness_filters(self):
        return {}

    def get_normalized_hotness(self):
        queryset = type(self).objects.filter(**self.get_hotness_filters())
        print(queryset.aggregate(Max('hotness')))
        maximum = queryset.aggregate(Max('hotness'))['hotness__max']
        minimum = queryset.aggregate(Min('hotness'))['hotness__min']

        diff = maximum - minimum

        if diff == 0:
            return 0

        return (self.hotness - minimum) / (maximum - minimum)


class StripeAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stripe_accounts")
    code = models.CharField(max_length=255)
    account_id = models.CharField(max_length=255)
    business_name = models.CharField(max_length=100, default="")


class AnalyticsUser(models.Model):
    analytics_user_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)


class PriceGroup(HeatableModel):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    stripe_account = models.ForeignKey(StripeAccount, on_delete=models.CASCADE, related_name="groups", null=True, blank=True)
    stripe_id = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

    def get_smart_price(self):
        prices = list(self.prices.all().order_by("-hotness"))
        raw_hotness = list(self.prices.all().order_by("-hotness").values_list('hotness', flat=True))
        sum_raw = sum(raw_hotness)

        normalizer = 1 / (sum_raw if sum_raw > 0 else 1)

        normalized_hotness = [raw * normalizer for raw in raw_hotness]

        return choice(prices, len(prices), p=normalized_hotness)[0]

    def get_smart_description(self):
        descriptions_query = self.descriptions.all().order_by("-hotness")
        descriptions = list(descriptions_query)
        count = descriptions_query.count()
        raw_hotness = list(descriptions_query.values_list('hotness', flat=True))
        sum_raw = sum(raw_hotness)

        try:
            normalizer = 1 / (sum_raw if sum_raw > 0 else 0)
        except Exception:
            return None

        normalized_hotness = [raw * normalizer for raw in raw_hotness]

        return choice(descriptions, count, p=normalized_hotness)[0]

    def get_smart_features(self):
        slots = self.slots.all()
        features = []

        for slot in slots:
            features.append(slot.get_smart_feature())

        return features

    def get_description_by_user(self, user):
        description = self.descriptions.filter(users__in=[user]).first()

        return description

    def get_price_by_user(self, user):
        price = self.prices.filter(users__in=[user]).first()

        return price

    def get_features_by_user(self, user):
        features = GroupFeature.objects.filter(slot__group=self, users__in=[user])

        return features

class PriceGroupDescription(HeatableModel):
    description = models.TextField()
    group = models.ForeignKey(PriceGroup, on_delete=models.CASCADE, default="description", related_name="descriptions")
    users = models.ManyToManyField(AnalyticsUser, related_name="descriptions", blank=True)


class Price(HeatableModel):
    group = models.ForeignKey(PriceGroup, on_delete=models.CASCADE, related_name="prices")
    stripe_id = models.CharField(max_length=200)
    price = models.FloatField()
    users = models.ManyToManyField(AnalyticsUser, related_name="prices", blank=True)
    term = models.CharField(max_length=25, choices=Terms.choices, default=Terms.MONTHLY, null=True, blank=True)
    
    class Meta:
        ordering = ['group__name', 'price', 'term']

    def __str__(self):
        return f"{str(self.group)} - ${self.price} - {self.get_term_display()}"


class GroupFeatureSlot(models.Model):
    group = models.ForeignKey(PriceGroup, on_delete=models.CASCADE, related_name="slots")
    order = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order:
            greatest_slot = self.group.slots.all().order_by("-order").first()

            if greatest_slot:
                self.order = greatest_slot.order + 1
            else:
                self.order = 1
        
        super(GroupFeatureSlot, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.group.name} - {self.order}"

    def get_smart_feature(self):
        features_query = self.features.all().order_by("-hotness")
        features = list(features_query)
        raw_hotness = list(features_query.values_list('hotness', flat=True))
        sum_raw = sum(raw_hotness)

        try:
            normalizer = 1 / (sum_raw if sum_raw > 0 else 0)
        except Exception:
            return None

        normalized_hotness = [raw * normalizer for raw in raw_hotness]

        return choice(features, len(features), p=normalized_hotness)[0]


class GroupFeature(HeatableModel):
    slot = models.ForeignKey(GroupFeatureSlot, on_delete=models.CASCADE, related_name="features", null=True)
    description = models.TextField()
    users = models.ManyToManyField(AnalyticsUser, related_name="features", blank=True)

    def __str__(self):
        return f"{self.slot.group.name} ({self.slot.order} - {self.description})"

class AnalyticRecord(models.Model):
    user = models.ForeignKey(AnalyticsUser, on_delete=models.CASCADE, related_name="user_analytics")
    action = models.CharField(choices=Actions.choices, max_length=100, default=Actions.BLANK)
    group = models.ForeignKey(PriceGroup, on_delete=models.CASCADE, related_name="group_analytics")
    price = models.ForeignKey(Price, on_delete=models.SET_NULL, related_name="price_analytics", null=True)
    group_description = models.ForeignKey(PriceGroupDescription, on_delete=models.SET_NULL, related_name="description_analytics", null=True)
    features = models.ManyToManyField(GroupFeature, related_name="feature_analytics")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.group.name} | {self.price.price} | {self.get_action_display()}"



