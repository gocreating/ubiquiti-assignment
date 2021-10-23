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

urlpatterns = [
    path('users/', handle_users),
]
