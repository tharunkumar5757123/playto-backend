from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from feed.views import PostViewSet, CommentViewSet, LeaderboardView

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/leaderboard/", LeaderboardView.as_view()),
]
