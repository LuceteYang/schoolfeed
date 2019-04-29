from rest_framework.views import APIView
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
class Schools(APIView):
    """Schools cbv classdoc"""
    serializer_class = serializers.SchoolsSerializer
    parser_classes = (MultiPartParser,)


    @swagger_auto_schema(
        operation_description="학교를 생성하는 API",
        responses={201: serializers.SchoolListSerializer(),400: '정보를 잘못 입력한 경우'},
        tags=['schools'],
        request_body=serializers.SchoolsSerializer()
    )
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
                role=1
            )
            models.Subscribe.objects.create(
                subscriber=user,
                school=school
            )
            return Response(data=serializers.SchoolListSerializer(school).data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Search(APIView):
    """Search cbv classdoc"""

    @swagger_auto_schema(
        operation_description="학교 검색 API",
        query_serializer=serializers.SearchQuerySerializer,
        responses={200: serializers.SchoolListSerializer(many=True)},
        tags=['schools']
    )
    def get(self, request, format=None):
        school_name = request.query_params.get('school_name',None)
        if school_name is None:
            print(school_name)
            schools = []
        else:    
            schools = models.School.objects.filter(name__contains=school_name, deleted_at__isnull=True)

        serializer = serializers.SchoolListSerializer(schools, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SchoolDetail(APIView):
    """SchoolDetail cbv classdoc"""
    
    serializer_class = serializers.SchoolDetailSerializer
    parser_classes = (MultiPartParser,)

    def find_managing_school(self, school_id, user):
        try:
            school = models.School.objects.get(id=school_id, deleted_at__isnull=True)
            models.Member.objects.get(school__id=school_id, member=user, role__gte=0)
            return school
        except (models.School.DoesNotExist, models.Member.DoesNotExist) as e:
            return None

    @swagger_auto_schema(
        operation_description="학교 페이지 정보를 불러오는 API",
        responses={200: serializers.SchoolListSerializer()},
        tags=['schools']
    )
    def get(self, request, school_id, format=None):

        user = request.user

        try:
            school = models.School.objects.get(id=school_id, deleted_at__isnull=True)
        except models.School.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.SchoolDetailSerializer(school, context={'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="학교 정보를 수정하는 API",
        responses={200: serializers.SchoolListSerializer(),400: '정보를 잘못 입력한 경우'},
        tags=['schools'],
        request_body=serializers.SchoolDetailSerializer()
    )
    def put(self, request, school_id, format=None):

        user = request.user

        school = self.find_managing_school(school_id, user)
        if school is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.SchoolDetailSerializer(school, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():

            serializer.save(school=school)

            return Response(data=serializers.SchoolListSerializer(school).data, status=status.HTTP_200_OK)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="학교를 삭제하는 API",
        tags=['schools'],
        responses={204: '학교 삭제 완료',400: '학교가 존재하지 않는 경우'}
    )
    def delete(self, request, school_id, format=None):

        user = request.user

        school = self.find_managing_school(school_id, user)
        if school is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        school.deleted_at = Now()
        school.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeSchool(APIView):
    """SubscribeSchool cbv classdoc"""

    @swagger_auto_schema(
        operation_description="학교를 구독한 유저들을 불러오는 API",
        responses={200: serializers.SchoolListSerializer()},
        tags=['schools']
    )
    def get(self, request, school_id, format=None):

        subscribes = models.Subscribe.objects.filter(school__id=school_id)

        subscribers_ids = subscribes.values('subscriber_id')

        users = user_models.User.objects.filter(id__in=subscribers_ids)

        serializer = user_serializers.ListUserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="유저가 학교를 구독하는 API",
        tags=['schools'],
        responses={201: '구독 완료',304: '이미 구독 했던 경우', 404: '학교를 찾을수 없음'}
    )
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
    @swagger_auto_schema(
        operation_description="유저가 학교를 구독 취소하는 API",
        tags=['schools'],
        responses={204: '구독 취소 완료',304: '구독하지 않았던 경우'}
    )
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
        operation_description="학교의 컨텐츠 리스트를 불러오는 API",
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
        serializer = contents_serializers.ContentsSerializer(contents, many=True, context={'request': request})
        return Response(data=serializer.data)

        