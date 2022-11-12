import random
from django.core.management.base import BaseCommand, CommandError
from core.models import PriceGroup, PriceGroupDescription, GroupFeatureSlot, GroupFeature, Price

groups = [
    "Basic",
    "SMB",
    "Enterprise"
]

descriptions = [
    "Price Title 1",
    "Price Title 2",
    "Price Title 3",
    "Price Title 4",
    "Price Title 5",
    "Price Title 6",
    "Price Title 7",
    "Price Title 8",
    "Price Title 9",
    "Price Title 10",
]
features = [
    "Awesome Feature 1",
    "Awesome Feature 2",
    "Awesome Feature 3",
    "Awesome Feature 4",
    "Awesome Feature 5",
    "Awesome Feature 6",
    "Awesome Feature 7",
    "Awesome Feature 8",
    "Awesome Feature 9",
    "Awesome Feature 10",
    "Awesome Feature 11",
]

PRICES = [
    [5.99, 9.99, 14.99],
    [19.99, 24.99, 29.99],
    [49.99, 199.99, 499.99]
]

class Command(BaseCommand):

    def handle(self, *args, **options):
        PriceGroupDescription.objects.all().delete()
        GroupFeatureSlot.objects.all().delete()
        GroupFeature.objects.all().delete()
        Price.objects.all().delete()
        PriceGroup.objects.all().delete()

        for group in groups:
            PriceGroup.objects.create(
                name=group
            )

        for group in PriceGroup.objects.all():
            price_list = random.choice(PRICES)
            for price in price_list:
                Price.objects.create(
                    group=group,
                    stripe_id="abc1234",
                    price=price
                )
            for y in range(5):
                PriceGroupDescription.objects.create(
                    description=f"{group.name} ({y}) - {random.choice(descriptions)}",
                    group=group
                )
            for i in range(4):
                slot = GroupFeatureSlot.objects.create(
                    group=group,
                    order=i
                )
                for x in range(3):
                    GroupFeature.objects.create(
                        slot=slot,
                        description=f"{group.name} ({i}/{x}): {random.choice(features)}"
                    )

