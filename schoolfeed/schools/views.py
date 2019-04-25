from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from . import models, serializers
from rest_framework.parsers import FormParser, MultiPartParser
from schoolfeed.users import models as user_models
from schoolfeed.contents import models as contents_models
from schoolfeed.users import serializers as user_serializers
from schoolfeed.contents import serializers as contents_serializers
from django.db.models.functions import Now

from drf_yasg.utils import swagger_auto_schema


# Create your views here.
class Schools(GenericAPIView):
    """
        학교 리스트와 생성하는 API

        ---
        # 내용
            - position : 생성자 직책
            - name : 학교 이름
            - image : 학교 사진
            - location : 학교 위치
    """
    serializer_class = serializers.SchoolsSerializer
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request, format=None):
        
        user = request.user

        schools = models.School.objects.all()

        serializer = serializers.SchoolListSerializer(schools, many=True)

        return Response(data=serializer.data)

    def post(self, request, format=None):

        user = request.user  

        serializer = serializers.SchoolsSerializer(data=request.data)
        if serializer.is_valid():
            school = models.School.objects.create(
                name=request.data.get('name'),
                image=request.data.get('image',None),
                location=request.data.get('location',None),
                creator=user
              )
            models.Member.objects.create(
                school=school,
                member=user,
                position=request.data.get('position'),
                role=1
            )
            models.Subscribe.objects.create(
                subscriber=user,
                school=school
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SchoolDetail(GenericAPIView):
    """
        학교 정보를 조회, 수정, 삭제하는  API
        
        ---
        # 내용
            - profile_image : 프로필 이미지
            - username : 유져 아이디
            - name : 유져 이름
    """
    
    serializer_class = serializers.SchoolDetailSerializer
    parser_classes = (FormParser, MultiPartParser)
    def find_managing_school(self, school_id, user):
        try:
            school = models.School.objects.get(id=school_id, deleted_at__isnull=True)
            models.Member.objects.get(school__id=school_id, member=user, role__gte=0)
            return school
        except (models.School.DoesNotExist, models.Member.DoesNotExist) as e:
            return None

    def get(self, request, school_id, format=None):

        user = request.user

        try:
            school = models.School.objects.get(id=school_id, deleted_at__isnull=True)
        except models.School.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.SchoolDetailSerializer(school, context={'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, school_id, format=None):

        user = request.user

        school = self.find_managing_school(school_id, user)
        if school is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.SchoolDetailSerializer(school, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save(school=school)

            return Response(status=status.HTTP_204_NO_CONTENT)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, school_id, format=None):

        user = request.user

        school = self.find_managing_school(school_id, user)
        if school is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        school.deleted_at = Now()
        school.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeSchool(APIView):

    def get(self, request, school_id, format=None):

        subscribes = models.Subscribe.objects.filter(school__id=school_id)

        subscribers_ids = subscribes.values('subscriber_id')

        users = user_models.User.objects.filter(id__in=subscribers_ids)

        serializer = user_serializers.ListUserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, school_id, format=None):
        user = request.user

        try:
            found_school = models.School.objects.get(id=school_id, deleted_at__isnull=True)
        except models.School.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            preexisiting_subscibes = models.Subscribe.objects.get(
                subscriber=user,
                school=found_school
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except models.Subscribe.DoesNotExist:

            new_subscribe = models.Subscribe.objects.create(
                subscriber=user,
                school=found_school
            )

            new_subscribe.save()
            return Response(status=status.HTTP_201_CREATED)

class UnSubscribeSchool(APIView):

    def delete(self, request, school_id, format=None):

        user = request.user

        try:
            preexisiting_subscibes = models.Subscribe.objects.get(
                subscriber=user,
                school__id=school_id
            )
            preexisiting_subscibes.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Subscribe.DoesNotExist:

            return Response(status=status.HTTP_304_NOT_MODIFIED)


class ContentsSchool(APIView):

    @swagger_auto_schema(
        query_serializer=serializers.ContentsQuerySerializer
    )
    def get(self, request, school_id, format=None):
        try:
            last_contents_id = int(request.GET.get('last_contents_id'))
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        field_value_pairs = [('school__id', school_id),('deleted_at__isnull', True)]
        if last_contents_id>0:
            field_value_pairs.append(('id__lt', last_contents_id))
        filter_options = {k:v for k,v in field_value_pairs if v}
        contents =  contents_models.Contents.objects.filter(
                                    **filter_options
                                ).order_by('-id')[:10]
        serializer = contents_serializers.ContentsSerializer(contents, many=True)
        return Response(data=serializer.data)

        