from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from meiduo import settings

s = Serializer(secret_key=settings.SECRET_KEY, expires_in=None)