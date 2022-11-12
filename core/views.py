from django.views.generic.base import TemplateView
import stripe
import pandas as pd
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Price, PriceGroup, PriceGroupDescription, StripeAccount
from .choices import Terms

from app.models import Component


class RenderWidgetView(TemplateView):
    """
    Connect Stripe TemplateView
    """

    
    template_name = "core/index.html"


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e

        stripe_account = StripeAccount.objects.get(account_id=event.account)

        # Handle the event
        if event['type'] == 'price.created':
            price = event['data']['object']

            price_group = PriceGroup.objects.get(stripe_id=price["product"])

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
        elif event['type'] == 'price.deleted':
            price = event['data']['object']
        elif event['type'] == 'price.updated':
            price = event['data']['object']
        elif event['type'] == 'product.created':
            product = event['data']['object']
            group = PriceGroup.objects.create(
                name=product["name"],
                stripe_account=stripe_account,
                stripe_id=product["id"],
            )

            if product["description"]:
                PriceGroupDescription.objects.create(
                    group=group,
                    description=product["description"]
                )
        elif event['type'] == 'product.deleted':
            product = event['data']['object']
        elif event['type'] == 'product.updated':
            product = event['data']['object']
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event['type']))

        return HttpResponse(status=200)