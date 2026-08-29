from django.urls import path
from .views import LoginAPI, LogoutAPI, ProfileAPI
from .views import admin_dashboard
urlpatterns=[
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('profile/', ProfileAPI.as_view()),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
]