from functools import wraps

from firebase_admin import auth
from firebase_admin._auth_utils import InvalidIdTokenError
from firebase_admin._token_gen import ExpiredIdTokenError
from flask import request

from services.user import get_user_by_id


def authorization_required(admin_required=False, is_owner=False):
    def decorator(f):
        """A decorator that only allows access to requests with a valid token."""

        @wraps(f)
        def wrapper(*args, **kwargs):
            # print(roles)
            header_token = request.headers.get('Authorization')
            if header_token is None or "":
                return dict(message='Token required.'), 401

            try:
                uid = auth.verify_id_token(header_token).get('uid')
                user_record = auth.get_user(uid)
                current_user, detail = get_user_by_id(uid)

                if admin_required and current_user.role != 'admin':
                    return dict(message='admin required.'), 401

                return f(*args, **{**kwargs, **{'current_user': current_user}})
            except ExpiredIdTokenError as e:
                return dict(message=str(e)), 403
            except (InvalidIdTokenError, ValueError) as e:
                return dict(message=str(e)), 401

        return wrapper

    return decorator
