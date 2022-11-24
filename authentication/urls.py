from django.urls import path

from rest_framework.authtoken import views
from authentication.views import UserCreateView, Logout

urlpatterns = [
    path('create/', UserCreateView.as_view()),
    path('login/', views.obtain_auth_token),
    path('logout/', Logout.as_view())
]
