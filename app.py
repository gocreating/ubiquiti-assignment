import json
from urllib.parse import parse_qs

from django.http import JsonResponse
from django.urls import path

from config import ACCESS_TOKEN_COOKIE_KEY
from decorators import login_required, managed_transaction
from models.user import User


DEBUG = True
SECRET_KEY = '4l0ngs3cr3tstr1ngw3lln0ts0l0ngw41tn0w1tsl0ng3n0ugh'
ROOT_URLCONF = __name__

@managed_transaction
@login_required
def list_users(request):
    users = request.session.query(User).all()
    return JsonResponse([user.to_dict() for user in users], safe=False)

@managed_transaction
def create_user(request):
    data = json.loads(request.body)
    user = User(**data)
    request.session.add(user)
    request.session.flush()
    return JsonResponse(user.to_dict(), safe=False)

def handle_users(request):
    if request.method == 'GET':
        return list_users(request)
    elif request.method == 'POST':
        return create_user(request)

@managed_transaction
@login_required
def search_user(request):
    if request.method == 'GET':
        query_string = request.GET.urlencode()
        query = parse_qs(query_string)
        filtered_user = request.session.query(User)\
            .filter(User.fullname == query['fullname'][0])\
            .first()
        if filtered_user is None:
            return JsonResponse(None, safe=False)
        return JsonResponse(filtered_user.to_dict(), safe=False)

@managed_transaction
def signin_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.session.query(User)\
            .filter(User.acct == data['acct'], User.pwd == data['pwd'])\
            .one_or_none()
        if user is None:
            return JsonResponse(None, status=401, safe=False)

        access_token = user.generate_jwt()
        response = JsonResponse(user.to_dict(), safe=False)
        response.set_cookie(ACCESS_TOKEN_COOKIE_KEY, access_token)
        return response

@managed_transaction
@login_required
def handle_user(request, user_id):
    if request.method == 'GET':
        user = request.session.query(User).get(user_id)
        if user is None:
            return JsonResponse(None, safe=False)
        return JsonResponse(user.to_dict(), safe=False)

urlpatterns = [
    path('users/', handle_users),
    path('users/search/', search_user),
    path('users/signin/', signin_user),
    path('users/<int:user_id>/', handle_user),
]
