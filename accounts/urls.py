from django.urls import path
from .views import LoginAPI, LogoutAPI, ProfileAPI
urlpatterns=[
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('profile/', ProfileAPI.as_view()),
]