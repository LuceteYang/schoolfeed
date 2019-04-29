from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from . import models

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'profile_image',
            'name',
            'email',
        )

class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'profile_image',
            'name',
        )


class SignUpSerializer(RegisterSerializer):

    name = serializers.CharField(required=True, write_only=True)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'name': self.validated_data.get('name', ''),
            'email': self.validated_data.get('email', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        user.save()
        return user

class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(read_only=True)
    
class PageQuerySerializer(serializers.Serializer):
    page = serializers.IntegerField(help_text="리스트의 page 값, 초기값 : 1", required=True)
    
class ContentsQuerySerializer(serializers.Serializer):
    last_contents_id = serializers.IntegerField(help_text="컨텐츠 리스트의 마지막 contents id 값 초기값 : 0", required=True)

