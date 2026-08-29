from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Programme
from accounts.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated


class ProgrammeList(APIView):
    permission_classes=[IsAuthenticated, IsAdmin]
    def get(self, r):
        data=list(Programme.objects.values())
        return Response(data)
urlpatterns=[path('programmes/', ProgrammeList.as_view())]