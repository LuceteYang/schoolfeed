from rest_framework import serializers
from schoolfeed.users import serializers as users_serializers
from . import models
from schoolfeed.schools import models as schools_models

class SchoolListSerializer(serializers.ModelSerializer):

	name = serializers.CharField(required=False)
	image = serializers.FileField(required=False)
	location = serializers.CharField(required=False)

	class Meta:
		model = schools_models.School
		fields = (
			'id',
			'name',
			'image',
			'location',
		)

class ContentsSerializer(serializers.ModelSerializer):
	
	creator = users_serializers.ListUserSerializer(read_only=True)
	school = SchoolListSerializer(read_only=True)
	class Meta:
		model = models.Contents
		fields = (
			'id',
			'creator',
			'main_image',
			'text',
			'school',
			'natural_time'
			) 

class InputContentsSerializer(serializers.ModelSerializer):
	
	text = serializers.CharField(required=True)
	creator = users_serializers.ListUserSerializer(read_only=True)

	class Meta:
		model = models.Contents
		fields = (
			'id',
			'creator',
			'main_image',
			'text',
			'school',
			) 

class ContentsQuerySerializer(serializers.Serializer):
    last_contents_id = serializers.IntegerField(help_text="this field is generated from a query_serializer", required=True)
