from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from rest_framework.parsers import FormParser, MultiPartParser
from schoolfeed.schools import models as schools_models
from django.db.models.functions import Now

from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class Contents(APIView):
	"""Contents cbv classdoc"""

	serializer_class = serializers.InputContentsSerializer
	parser_classes = (FormParser, MultiPartParser)

	@swagger_auto_schema(
		operation_description="컨텐츠를 생성하는 API",
		responses={200: serializers.InputContentsSerializer(),400: '정보를 잘못 입력한 경우'},
		tags=['contents'],
		request_body=serializers.InputContentsSerializer()
	)
	def post(self, request, format=None):

		user = request.user

		serializer = serializers.InputContentsSerializer(data=request.data)
		if serializer.is_valid():
			try:
				role = schools_models.Member.objects.get(school__id=request.data.get('school'), member=user, role__gte=0)
			except (schools_models.Member.DoesNotExist) as e:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			serializer.save(creator=user)
			return Response(serializer.data,status=status.HTTP_200_OK)

		else:
			return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContentsDetail(APIView):
	"""ContentsDetail cbv classdoc"""
	
	serializer_class = serializers.InputContentsSerializer
	parser_classes = (FormParser, MultiPartParser)

	def find_managing_school(self, school_id, user):
		try:
			school = schools_models.School.objects.get(id=school_id, deleted_at__isnull=True)
			schools_models.Member.objects.get(school__id=school_id, member=user, role__gte=0)
			return school
		except (schools_models.School.DoesNotExist, schools_models.Member.DoesNotExist) as e:
			return None
	
	@swagger_auto_schema(
		operation_description="컨텐츠 상세보기 API",
		responses={200: serializers.ContentsSerializer(),400: '해당 컨텐츠가 없는 경우'},
		tags=['contents']
	)
	def get(self, request, contents_id, format=None):

		user = request.user

		try:
			contents = models.Contents.objects.select_related('school','creator').get(id=contents_id, deleted_at__isnull=True)
		except models.Contents.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = serializers.ContentsSerializer(contents, context={'request': request})

		return Response(data=serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="컨텐츠 수정 API",
		responses={200: serializers.InputContentsSerializer(),400: '정보를 잘못 입력한 경우'},
		tags=['contents'],
		request_body=serializers.InputContentsSerializer()
	)
	def put(self, request, contents_id, format=None):

		user = request.user
		try:
			contents = models.Contents.objects.get(id=contents_id, deleted_at__isnull=True)
		except models.Contents.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = serializers.InputContentsSerializer(contents,data=request.data, partial=True)

		if serializer.is_valid():
			school = self.find_managing_school(contents.school.id, user)
			if school is None:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)

		else:
			return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="컨텐츠 삭제 API",
		responses={204: "삭제 성공"},
		tags=['contents']
	)
	def delete(self, request, contents_id, format=None):

		user = request.user
		try:
			contents = models.Contents.objects.get(id=contents_id, deleted_at__isnull=True)
		except models.Contents.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		school = self.find_managing_school(contents.school.id, user)
		if school is None:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		contents.deleted_at = Now()
		contents.save()
		return Response(status=status.HTTP_204_NO_CONTENT)
