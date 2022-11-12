from django.views.generic.base import TemplateView


class DocumentationView(TemplateView):
    """
    Connect Stripe TemplateView
    """
    
    template_name = "api/index.html"