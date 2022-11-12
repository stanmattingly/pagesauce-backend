from core.models import Price, GroupFeature, PriceGroupDescription

def set_price_hotness():
    for price in Price.objects.all():
        price.set_hotness()

def set_features_hotness():
    for feature in GroupFeature.objects.all():
        feature.set_hotness()

def set_description_hotness():
    for desc in PriceGroupDescription.objects.all():
        desc.set_hotness()

def update_hotness():
    set_price_hotness()
    set_features_hotness()
    set_description_hotness()