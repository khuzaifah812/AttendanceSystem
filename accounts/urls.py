from django.urls import path
from .views import custom_logout, custom_login, admin_dashboard
from .views import LoginAPI, LogoutAPI, ProfileAPI

urlpatterns=[
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='web_logout'),
    path('api-logout/', LogoutAPI.as_view(), name='api_logout'),
    path('api-login/', LoginAPI.as_view(), name='api_login'),
    path('profile/', ProfileAPI.as_view()),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
]