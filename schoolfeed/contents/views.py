from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from rest_framework.parsers import FormParser, MultiPartParser
from schoolfeed.schools import models as schools_models
from django.db.models.functions import Now

from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class Contents(GenericAPIView):
	"""
		구독한 학교 컨텐츠 리스트와 생성하는 API

		---
		# 내용
			- id : 컨텐츠 아이디
			- school : 학교
			- creator : 컨텐츠 작성자
			- main_image : 컨텐츠 사진
			- text : 컨텐츠 내용
	"""
	serializer_class = serializers.InputContentsSerializer
	parser_classes = (FormParser, MultiPartParser)

	@swagger_auto_schema(
		query_serializer=serializers.ContentsQuerySerializer
	)
	def get(self, request, format=None):
		try:
			last_contents_id = int(request.GET.get('last_contents_id'))
		except:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		user = request.user
		subscibed_schools_ids = schools_models.Subscribe.objects.filter(subscriber=user.id).values('school')
		field_value_pairs = [('school__id__in', subscibed_schools_ids),('deleted_at__isnull', True)]
		if last_contents_id>0:
			field_value_pairs.append(('id__lt', last_contents_id))
		filter_options = {k:v for k,v in field_value_pairs if v}
		contents =  models.Contents.objects.filter(
									**filter_options
								).order_by('-id')[:10]
		serializer = serializers.ContentsSerializer(contents, many=True)
		return Response(data=serializer.data)

	def post(self, request, format=None):

		user = request.user

		serializer = serializers.InputContentsSerializer(data=request.data)
		if serializer.is_valid():
			try:
				role = schools_models.Member.objects.get(school__id=request.data.get('school'), member=user, role__gte=0)
			except (schools_models.Member.DoesNotExist) as e:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			serializer.save(creator=user)
			return Response(status=status.HTTP_201_CREATED)

		else:
			return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContentsDetail(GenericAPIView):
	"""
		컨텐츠 정보를 조회, 수정, 삭제하는  API
		
		---
		# 내용
			- id : 컨텐츠 아이디
			- school : 학교
			- creator : 컨텐츠 작성자
			- main_image : 컨텐츠 사진
			- text : 컨텐츠 내용
	"""
	
	serializer_class = serializers.InputContentsSerializer
	parser_classes = (FormParser, MultiPartParser)
	def find_managing_school(self, school_id, user):
		try:
			school = schools_models.School.objects.get(id=school_id, deleted_at__isnull=True)
			schools_models.Member.objects.get(school__id=school_id, member=user, role__gte=0)
			return school
		except (schools_models.School.DoesNotExist, schools_models.Member.DoesNotExist) as e:
			return None

	def get(self, request, contents_id, format=None):

		user = request.user

		try:
			contents = models.Contents.objects.get(id=contents_id, deleted_at__isnull=True)
		except models.Contents.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = serializers.ContentsSerializer(contents)

		return Response(data=serializer.data, status=status.HTTP_200_OK)

	def put(self, request, contents_id, format=None):

		user = request.user
		try:
			contents = models.Contents.objects.get(id=contents_id, deleted_at__isnull=True)
		except models.Contents.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = serializers.InputContentsSerializer(contents,data=request.data, partial=True)

		if serializer.is_valid():
			print(contents.school.id)
			school = self.find_managing_school(contents.school.id, user)
			if school is None:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			serializer.save()
			return Response(status=status.HTTP_204_NO_CONTENT)

		else:
			print(serializer.errors)
			return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
