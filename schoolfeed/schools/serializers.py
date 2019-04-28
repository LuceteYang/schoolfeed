from rest_framework import serializers
from . import models
from schoolfeed.contents import models as contents_models
from schoolfeed.contents import serializers as contents_serializers


class SchoolsSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	name = serializers.CharField(required=True)
	image = serializers.FileField(required=False)
	location = serializers.CharField(required=False)

class SchoolDetailSerializer(serializers.ModelSerializer):
	contents = serializers.SerializerMethodField('paginated_contents')
	name = serializers.CharField(required=False)
	image = serializers.FileField(required=False)
	location = serializers.CharField(required=False)
	is_subscribed = serializers.SerializerMethodField()
	is_manager = serializers.SerializerMethodField()

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
	def paginated_contents(self, obj):
		
		contents = contents_models.Contents.objects.filter(
									school=obj.id,
									deleted_at__isnull=True
								).order_by('-id')[:10]
		if 'request' in self.context:
			request = self.context['request']
			serializer = contents_serializers.ContentsSerializer(contents,many=True, context={'request': request})
		else:
			serializer = contents_serializers.ContentsSerializer(contents,many=True)
		return serializer.data
	def get_is_subscribed(self, obj):
		if 'request' in self.context:
			request = self.context['request']
			try:
				models.Subscribe.objects.get(subscriber__id=request.user.id, school__id=obj.id)
				return True
			except models.Subscribe.DoesNotExist:
				return False
		return False
	def get_is_manager(self, obj):
		if 'request' in self.context:
			request = self.context['request']
			try:
				models.Member.objects.get(member__id=request.user.id, school__id=obj.id, role__gte=0)
				return True
			except models.Member.DoesNotExist:
				return False
		return False

class SchoolListSerializer(serializers.ModelSerializer):

	name = serializers.CharField(required=False)
	image = serializers.FileField(required=False)
	location = serializers.CharField(required=False)
	is_subscribed = serializers.SerializerMethodField()

	class Meta:
		model = models.School
		fields = (
			'id',
			'name',
			'image',
			'location',
			'is_subscribed',
		)
	def get_is_subscribed(self, obj):
		if 'request' in self.context:
			request = self.context['request']
			try:
				models.Subscribe.objects.get(subscriber__id=request.user.id, school__id=obj.id)
				return True
			except models.Subscribe.DoesNotExist:
				return False
		return False

class ContentsQuerySerializer(serializers.Serializer):
	last_contents_id = serializers.IntegerField(help_text="this field is generated from a query_serializer", required=True)
	
class PageQuerySerializer(serializers.Serializer):
	page = serializers.IntegerField(help_text="this field is generated from a query_serializer", required=True)

class SearchQuerySerializer(serializers.Serializer):
	school_name = serializers.CharField(help_text="this field is generated from a query_serializer", required=True)
