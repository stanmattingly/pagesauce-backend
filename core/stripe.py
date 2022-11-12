from pydoc import describe
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

from .models import PriceGroup, Price, PriceGroupDescription
from .choices import Terms


def get_account_id_from_code(code):
    return stripe.OAuth.token(
        grant_type='authorization_code',
        code=code,
    )['stripe_user_id']

def get_stripe_business_name(account_id):
    account_object = stripe.Account.retrieve(account_id)
    return account_object['settings']['dashboard']['display_name']

def sync_stripe_account(stripe_account):
    products = stripe.Product.list(stripe_account=stripe_account.account_id, active=True)

    for product in products.auto_paging_iter():
        price_group = PriceGroup.objects.create(
            name=product["name"],
            stripe_account=stripe_account,
            stripe_id=product["id"],
        )
        if product["description"]:
            PriceGroupDescription.objects.create(
                description=product["description"],
                group=price_group
            )
        prices = stripe.Price.list(product=product['id'], stripe_account=stripe_account.account_id)
        for price in prices.auto_paging_iter():
            cent_price = price['unit_amount']

            if cent_price:
                display_price = cent_price / 100
            else:
                display_price = 0

            Price.objects.create(
                group=price_group,
                stripe_id=price['id'],
                price=display_price,
                term=Terms.MONTHLY if price["type"] == "recurring" and price["recurring"]["interval"] == "month" else Terms.YEARLY if price["type"] == "recurring" and price["recurring"]["interval"] == "year" else Terms.ONE_TIME
            )

