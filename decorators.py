import functools
import jwt

from django.http import JsonResponse

from config import ACCESS_TOKEN_COOKIE_KEY, CSRF_TOKEN_COOKIE_KEY, CSRF_TOKEN_HEADER_KEY
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


def double_submit_csrf_token_required(func):

    @functools.wraps(func)
    def middleware(request, *args, **kwargs):
        csrf_token_in_cookie = request.COOKIES.get(CSRF_TOKEN_COOKIE_KEY)
        csrf_token_in_header = request.headers.get(CSRF_TOKEN_HEADER_KEY)
        if csrf_token_in_cookie is None or csrf_token_in_header is None or csrf_token_in_cookie != csrf_token_in_header:
            return JsonResponse(None, status=403, safe=False)

        response = func(request, *args, **kwargs)
        return response

    return middleware
