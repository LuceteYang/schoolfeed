import os

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View


class ReactAppView(View):

    def get(self, request):
        print(os.path.join(str(settings.ROOT_DIR), 'frontend', 'build', 'index.html'))
        try:
            with open(os.path.join(str(settings.ROOT_DIR), 'frontend', 'build', 'index.html')) as file:
                return HttpResponse(file.read())
        except IOError:
            return HttpResponse(
                """
                index.html not found ! build your React app !!
                """,
                status=501,
            )
