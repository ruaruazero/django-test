from wsgiref.util import request_uri

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from oAuth.models import User


# Create your views here.
class UserInfoViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_info = User.objects.filter(user_phone=request.user).values()[0]
        return_info = {
            'roles': user_info['roles'], # 是否是管理员
            'is_staff': user_info['is_staff'], # 是否是员工
            'is_member': user_info['is_member'] == 0, # 是否是会员
            'user_phone': user_info['user_phone'], # 手机号
            'nickname': user_info['nickname'], # 昵称
            'member_id': user_info['id']
        }
        return Response(return_info)