from rest_framework import serializers
from . import models

class ContentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Contents
        fields = '__all__' 