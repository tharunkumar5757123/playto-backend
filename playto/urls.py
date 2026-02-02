from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from feed.views import PostViewSet, CommentViewSet, LeaderboardView, home, like_post
from django.contrib.auth import views as auth_views

# DRF router
router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/leaderboard/", LeaderboardView.as_view()),
    
    # Home page
    path("", home, name="home"),
    
    # Django login
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    
    # Like post via Django view (to avoid JSON page)
    path("posts/<int:post_id>/like/", like_post, name="like_post"),
]
