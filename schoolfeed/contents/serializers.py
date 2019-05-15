from rest_framework import serializers
from schoolfeed.users import serializers as users_serializers
from . import models
from schoolfeed.schools import models as schools_models

from drf_yasg.utils import swagger_serializer_method

class ContentsSchoolListSerializer(serializers.ModelSerializer):

	class Meta:
		model = schools_models.School
		fields = (
			'id',
			'name',
			'image',
			'location',
		)

class ContentsSerializer(serializers.ModelSerializer):
	
	creator = users_serializers.ListUserSerializer(read_only=True, help_text="컨텐츠 작성 유저")
	school = ContentsSchoolListSerializer(read_only=True, help_text="컨텐츠 작성 학교")
	is_mine= serializers.SerializerMethodField(help_text="컨텐츠 소유 여부")
	class Meta:
		model = models.Contents
		fields = (
			'id',
			'creator',
			'main_image',
			'text',
			'school',
			'natural_time',
			'is_mine'
			)

	@swagger_serializer_method(serializer_or_field=serializers.BooleanField)
	def get_is_mine(self, contents):
		if 'request' in self.context:
			
			request =  self.context['request']
			# foreignKey일 경우 .id로 하면 쿼리로 한번더 검색
			if contents.creator_id == request.user.id:
				return True
			else:
				return False
		return False

class InputContentsSerializer(serializers.ModelSerializer):
	
	text = serializers.CharField(help_text="컨텐츠 내용", required=True)
	creator = users_serializers.ListUserSerializer(help_text="컨텐츠 작성자", read_only=True)

	class Meta:
		model = models.Contents
		fields = (
			'id',
			'creator',
			'main_image',
			'text',
			'school',
			) 

