import functools
import jwt

from django.http import JsonResponse

from config import ACCESS_TOKEN_COOKIE_KEY
from db import database
from models.user import User


def managed_transaction(func):

    @functools.wraps(func)
    def middleware(request, *args, **kwargs):
        session = database.get_session()
        try:
            request.session = session
            response = func(request, *args, **kwargs)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return response

    return middleware


def login_required(func):

    @functools.wraps(func)
    def middleware(request, *args, **kwargs):
        access_token = request.COOKIES.get(ACCESS_TOKEN_COOKIE_KEY)
        if access_token is None:
            return JsonResponse(None, status=401, safe=False)

        try:
            current_user = User.get_by_jwt(request.session, access_token)
            if current_user is None:
                return JsonResponse(None, status=401, safe=False)
            request.current_user = current_user
        except jwt.ExpiredSignatureError:
            return JsonResponse(None, status=401, safe=False)
        except:
            return JsonResponse(None, status=403, safe=False)

        response = func(request, *args, **kwargs)
        return response

    return middleware
