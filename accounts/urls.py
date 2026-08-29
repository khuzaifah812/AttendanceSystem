from django.urls import path
from .views import LoginAPI, LogoutAPI, ProfileAPI, custom_login, admin_dashboard

urlpatterns=[
    # WEB login - for browser form at /accounts/login/
    path('login/', custom_login, name='login'),
    
    # API login - for mobile/app
    path('api-login/', LoginAPI.as_view(), name='api_login'),
    
    path('logout/', LogoutAPI.as_view()),
    path('profile/', ProfileAPI.as_view()),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
]