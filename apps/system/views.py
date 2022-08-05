from django.shortcuts import render
from .models import FormalBug,SyetemQuestion
from .serializers import FormalBugSerializer,SyetemQuestionSerializer
from ..users.authorizations import JWTAuthentication
from ..users.permission import MyPermission
from utils.pagination import MyPageNumberPagination
from rest_framework.viewsets import ModelViewSet
from lwjTest.settings import logger
import os
from rest_framework.views import APIView
from utils.apiResponse import ApiResponse
from django_filters.rest_framework import DjangoFilterBackend
class FormalbugViewsets(ModelViewSet):
    """
    现网问题
    """
    queryset = FormalBug.objects.all()
    serializer_class = FormalBugSerializer
    pagination_class = MyPageNumberPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyPermission]

class SystemQuestionViewsets(ModelViewSet):
    """
    系统问题
    """
    queryset = SyetemQuestion.objects.all()
    serializer_class = SyetemQuestionSerializer
    pagination_class = MyPageNumberPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyPermission]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('project')
