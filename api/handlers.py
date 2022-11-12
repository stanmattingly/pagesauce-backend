from corsheaders.signals import check_request_enabled
from urllib.parse import urlparse

from app.models import Website


def cors_allow_mysites(sender, request, **kwargs):
    if request.path.startswith("/auth/") or request.path.startswith("/api/token/"):
        return True

    origin_host = urlparse(request.headers["Origin"]).netloc.strip('www.')

    return Website.objects.filter(url__contains=origin_host).exists()

check_request_enabled.connect(cors_allow_mysites)