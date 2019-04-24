from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from . import models, serializers
from rest_framework.parsers import FormParser, MultiPartParser

User = get_user_model()


class UserProfile(GenericAPIView): 
    """
        유져 정보를 수정하거나 불러오는 API
        
        ---
        # 내용
            - profile_image : 프로필 이미지
            - username : 유져 아이디
            - name : 유져 이름
    """
    serializer_class = serializers.UserProfileSerializer
    parser_classes = (FormParser, MultiPartParser)
    def get(self, request, format=None):
        
        serializer = serializers.UserProfileSerializer(request.user, context={'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):

        user = request.user
        serializer = serializers.UserProfileSerializer(user, data=request.data, partial=True) # field중 꼭 다 채워야 되지 않게됨
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)