from urllib.parse import parse_qs

from django.http import JsonResponse
from django.urls import path

from decorators import managed_transaction
from models.user import User


DEBUG = True
SECRET_KEY = '4l0ngs3cr3tstr1ngw3lln0ts0l0ngw41tn0w1tsl0ng3n0ugh'
ROOT_URLCONF = __name__

@managed_transaction
def handle_users(request):
    if request.method == 'GET':
        users = request.session.query(User).all()
        return JsonResponse([user.to_dict() for user in users], safe=False)

@managed_transaction
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

urlpatterns = [
    path('users/', handle_users),
    path('users/search/', search_user),
]
