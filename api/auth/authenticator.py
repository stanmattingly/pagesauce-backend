from core.models import Token
from rest_framework.authentication import TokenAuthentication as RestTokenAuth


class TokenAuthentication(RestTokenAuth):
    model = Token