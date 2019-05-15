from rest_framework import serializers
from . import models
from schoolfeed.contents import models as contents_models
from schoolfeed.contents import serializers as contents_serializers

from drf_yasg.utils import swagger_serializer_method

class SchoolsSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	class Meta:
		model = models.School
		fields = (
			'id',
			'name',
			'image',
			'location'
		)

class SchoolDetailSerializer(serializers.ModelSerializer):

	is_subscribed = serializers.SerializerMethodField(help_text="유저의 학교 구독 여부")
	is_manager = serializers.SerializerMethodField(help_text="유저의 학교 매니져 여부")
	contents = serializers.SerializerMethodField('paginated_contents',help_text="학교 게시글 리스트")

	class Meta:
		model = models.School
		fields = (
			'id',
			'name',
			'image',
			'location',
			'is_subscribed',
			'is_manager',
			'subscriber_count',
			'contents',
		)

	@swagger_serializer_method(serializer_or_field=serializers.ListField)
	def paginated_contents(self, obj):
		
		contents = contents_models.Contents.objects.prefetch_related('school','creator').filter(
									school=obj.id,
									deleted_at__isnull=True
								).order_by('-id')[:10]
		if 'request' in self.context:
			request = self.context['request']
			serializer = contents_serializers.ContentsSerializer(contents,many=True, context={'request': request})
		else:
			serializer = contents_serializers.ContentsSerializer(contents,many=True)
		return serializer.data

	@swagger_serializer_method(serializer_or_field=serializers.BooleanField)
	def get_is_subscribed(self, obj):
		if 'request' in self.context:
			request = self.context['request']
			if request.user in obj.subscribe_user_set.all():
				return True
			else:
				return False
		return False

	@swagger_serializer_method(serializer_or_field=serializers.BooleanField)
	def get_is_manager(self, obj):
		if 'request' in self.context:
			request = self.context['request']
			if request.user in obj.member_user_set.filter(member__role__gte=0):
				return True
			else:
				return False
		return False

class SchoolListSerializer(serializers.ModelSerializer):

	is_subscribed = serializers.SerializerMethodField(help_text="유저의 학교 구독 여부")

	class Meta:
		model = models.School
		fields = (
			'id',
			'name',
			'image',
			'location',
			'is_subscribed'
		)
		
		
	@swagger_serializer_method(serializer_or_field=serializers.BooleanField)
	def get_is_subscribed(self, obj):
		if 'request' in self.context:
			request = self.context['request']
			if request.user in obj.subscribe_user_set.all():
				return True
			else:
				return False
		return False
		
class ContentsQuerySerializer(serializers.Serializer):
	last_contents_id = serializers.IntegerField(help_text="컨텐츠 리스트의 마지막 contents id 값 초기값 : 0", required=True)
	

class SearchQuerySerializer(serializers.Serializer):
	school_name = serializers.CharField(help_text="검색하고자 하는 학교 이름", required=True)

