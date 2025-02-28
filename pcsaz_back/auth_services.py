from hashlib import sha256
from pcsaz_back.settings import JWT_SECRET_KEY
from datetime import datetime, timedelta, timezone
import jwt


def hash_pass(password):
    myhash = sha256()
    myhash.update(password.encode("utf-8"))
    return myhash.hexdigest()


def generate_jwt(uid):
    payload = {
        'user_id': uid,
        'exp' : datetime.now(timezone.utc) + timedelta(hours=12)
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def decode_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY , algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')

    return payload