from rest_framework import serializers
from . import models
from schoolfeed.contents import serializers as contents_serializers


class SchoolsSerializer(serializers.Serializer):
	position = serializers.IntegerField(required=True)
	name = serializers.CharField(required=True)
	image = serializers.FileField(required=False)
	location = serializers.CharField(required=False)

class SchoolDetailSerializer(serializers.ModelSerializer):

	contents = contents_serializers.ContentsSerializer(many=True, read_only=True)
	name = serializers.CharField(required=False)
	image = serializers.FileField(required=False)
	location = serializers.CharField(required=False)

	class Meta:
		model = models.School
		fields = (
			'id',
			'name',
			'image',
			'location',
			'contents',
		)

class SchoolListSerializer(serializers.ModelSerializer):

	name = serializers.CharField(required=False)
	image = serializers.FileField(required=False)
	location = serializers.CharField(required=False)

	class Meta:
		model = models.School
		fields = (
			'id',
			'name',
			'image',
			'location',
		)

class ContentsQuerySerializer(serializers.Serializer):
    last_contents_id = serializers.IntegerField(help_text="this field is generated from a query_serializer", required=True)
    