from django.urls import path

from . import views

app_name = "contents"
urlpatterns = [
    path('', view=views.Contents.as_view(), name="contents"),
    path('<int:contents_id>/', view=views.ContentsDetail.as_view(), name="detail")
]
