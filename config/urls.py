from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from rest_auth.views import (LoginView, PasswordChangeView, LogoutView)
from django.views.decorators.csrf import csrf_exempt

# drf_yasg
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# reactApp
from schoolfeed import views

# drf_yasg setting
schema_view = get_schema_view(
   openapi.Info(
      title="SchoolFeed API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="jae6120@naver.com"),
      license=openapi.License(name="Yang"),
   ),
   validators=['flex'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # rest-auth login, registration
    # path('api/rest-auth/login/', LoginView.as_view(), name='rest_login'),
    # path('api/rest-auth/logout/', LogoutView.as_view(), name='rest_logout'),
    # path('api/rest-auth/password/change/', csrf_exempt(PasswordChangeView.as_view()), name='rest_password_change'),
    path('api/rest-auth/', include(("rest_auth.urls","rest_framework"),namespace="rest_framework")),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    # User management
    path('api/users/', include("schoolfeed.users.urls")),
    # School management
    path('api/schools/', include("schoolfeed.schools.urls")),
    # Content management
    path('api/contents/', include("schoolfeed.contents.urls")),
    
    # drf_yasg Swagger
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^', views.ReactAppView.as_view()),
]
if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
