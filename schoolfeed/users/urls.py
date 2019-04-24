from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
	path("", view=views.UserProfile.as_view(), name="user_info"),
]
