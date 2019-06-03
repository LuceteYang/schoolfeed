from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from schoolfeed.users import serializers as users_serializers

from . import models


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
    contents = serializers.SerializerMethodField('paginated_contents', help_text="학교 게시글 리스트")

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

        contents = models.Contents.objects.prefetch_related('school', 'creator').filter(
            school=obj.id,
            deleted_at__isnull=True
        ).order_by('-id')[:10]
        if 'request' in self.context:
            request = self.context['request']
            serializer = ContentsSerializer(contents, many=True, context={'request': request})
        else:
            serializer = ContentsSerializer(contents, many=True)
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


class ContentsSchoolListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.School
        fields = (
            'id',
            'name',
            'image',
            'location',
        )


class ContentsSerializer(serializers.ModelSerializer):

    creator = users_serializers.ListUserSerializer(read_only=True, help_text="컨텐츠 작성 유저")
    school = ContentsSchoolListSerializer(read_only=True, help_text="컨텐츠 작성 학교")
    is_mine = serializers.SerializerMethodField(help_text="컨텐츠 소유 여부")

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
            request = self.context['request']
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
        read_only_fields = ('school',)
        fields = (
            'id',
            'creator',
            'main_image',
            'text',
            'school',
        )
