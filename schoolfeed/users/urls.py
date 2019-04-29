from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
	path("", view=views.UserProfile.as_view(), name="info"),
	path("schools/", view=views.UserSchool.as_view(), name="schools"),
	path("contents/", view=views.UserSchoolContents.as_view(), name="contents"),
	
]
