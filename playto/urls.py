from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from feed.views import PostViewSet

router = DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
