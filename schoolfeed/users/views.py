from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from schoolfeed.schools import models as schools_models
from schoolfeed.schools import serializers as schools_serializers

from . import serializers

User = get_user_model()


class UserProfile(APIView):
    """UserProfile cbv classdoc"""

    serializer_class = serializers.UserProfileSerializer
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_description="유저 정보를 불러오는 API",
        responses={200: serializers.UserProfileSerializer(), 400: '정보를 잘못 입력한 경우'},
        tags=['users'],
    )
    def get(self, request, format=None):

        serializer = serializers.UserProfileSerializer(request.user, context={'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="유저 정보를 수정하는 API",
        responses={200: serializers.UserProfileSerializer()},
        tags=['users'],
        request_body=serializers.UserProfileSerializer()
    )
    def put(self, request, format=None):

        user = request.user
        serializer = serializers.UserProfileSerializer(user, data=request.data, partial=True) # field중 꼭 다 채워야 되지 않게됨
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSchool(APIView):

    @swagger_auto_schema(
        operation_description="유저가 구독한 학교 리스트를 불러오는 API",
        query_serializer=serializers.PageQuerySerializer,
        responses={200: schools_serializers.SchoolListSerializer(many=True)},
        tags=['users']
    )
    def get(self, request, format=None):

        user = request.user

        subscibed_schools_ids = schools_models.Subscribe.objects.filter(subscriber=user.id).values('school')
        school_list = schools_models.School.objects.filter(
            id__in=subscibed_schools_ids,
            deleted_at__isnull=True
        ).prefetch_related('subscribe_user_set').order_by('id')

        paginator = Paginator(school_list, 20) # Show 20 contacts per page

        page = request.GET.get('page')
        try:
            schools = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            schools = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            schools = []
        serializer = schools_serializers.SchoolListSerializer(schools, many=True, context={'request': request})
        return Response(data=serializer.data)


class UserSchoolContents(APIView):
    @swagger_auto_schema(
        operation_description="유저가 구독한 학교의 컨텐츠를 불러오는 API",
        query_serializer=serializers.ContentsQuerySerializer,
        responses={200: schools_serializers.ContentsSerializer(many=True)},
        tags=['users']
    )
    def get(self, request, format=None):
        try:
            last_contents_id = int(request.GET.get('last_contents_id'))
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        subscibed_schools_ids = schools_models.Subscribe.objects.filter(subscriber=user.id).values('school')
        field_value_pairs = [('school__in', subscibed_schools_ids), ('deleted_at__isnull', True)]
        if last_contents_id > 0:
            field_value_pairs.append(('id__lt', last_contents_id))
        filter_options = {k: v for k, v in field_value_pairs}
        # related를 하면 nestedSerializer할 경우 각각 쿼리를 날리지 않음
        contents = schools_models.Contents.objects.filter(
            **filter_options
        ).select_related('school', 'creator').order_by('-id')[:10]
        serializer = schools_serializers.ContentsSerializer(contents, many=True, context={'request': request})
        return Response(data=serializer.data)
