from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from meiduo1 import settings
from itsdangerous import BadData

def generic_active_email_url(id,email):

    s = Serializer(secret_key = settings.SECRET_KEY, expires_in=3600)

    data = {
        'id':id,
        'email':email
    }
    serect_data = s.dumps(data)

    return 'http://www.meiduo.site:8000/emailsactive/?token=%s' % serect_data.decode()

def check_active_token(token):

    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)

    try:
        data = s.loads(token)
    except BadData:
        return None
    else:
        return data