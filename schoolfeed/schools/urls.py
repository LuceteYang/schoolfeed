from django.urls import path

from . import views

app_name = "schools"
urlpatterns = [
    path('', view=views.Schools.as_view(), name="schools"),
    path('search/', view=views.Search.as_view(), name="search"),
    path('<int:school_id>/', view=views.SchoolDetail.as_view(), name="detail"),
    path('<int:school_id>/subscribes/', view=views.SubscribeSchool.as_view(), name="subscribes"),
    path('<int:school_id>/unsubscribes/', view=views.UnSubscribeSchool.as_view(), name="unsubscribes"),
    path('<int:school_id>/contents/', view=views.ContentsSchool.as_view(), name="contents"),
    path('<int:school_id>/contents/<int:contents_id>/', view=views.ContentsDetail.as_view(), name="contentsDetail")
]
