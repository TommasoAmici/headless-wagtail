from django.urls import path, re_path

from .api import api_router

urlpatterns = [
    path("api/v2/", api_router.urls),
]
