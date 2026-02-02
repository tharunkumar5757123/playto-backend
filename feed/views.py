from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Like, KarmaTransaction
from .serializers import PostSerializer, CommentSerializer


# ------------------- DRF API -------------------

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer

    @action(detail=True, methods=["POST"])
    def like(self, request, pk=None):
        user = request.user
        post = self.get_object()

        with transaction.atomic():
            like = Like.objects.filter(user=user, post=post, comment=None).first()
            if like:
                # User already liked → remove like
                like.delete()
                return Response({"detail": "Like removed"})
            else:
                # Add new like
                Like.objects.create(user=user, post=post, comment=None)
                KarmaTransaction.objects.create(user=post.author, points=5)
                return Response({"detail": "Post liked"})


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().order_by("created_at")
    serializer_class = CommentSerializer

    @action(detail=True, methods=["POST"])
    def like(self, request, pk=None):
        user = request.user
        comment = self.get_object()

        with transaction.atomic():
            like = Like.objects.filter(user=user, post=None, comment=comment).first()
            if like:
                like.delete()
                return Response({"detail": "Like removed"})
            else:
                Like.objects.create(user=user, post=None, comment=comment)
                KarmaTransaction.objects.create(user=comment.author, points=1)
                return Response({"detail": "Comment liked"})


class LeaderboardView(APIView):
    def get(self, request):
        since = timezone.now() - timezone.timedelta(hours=24)
        data = (KarmaTransaction.objects
                .filter(created_at__gte=since)
                .values("user__username")
                .annotate(points_sum=Sum("points"))
                .order_by("-points_sum")[:5])
        return Response(data)


# ------------------- Django Views -------------------
@login_required
def home(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Post.objects.create(
                author=request.user,
                content=content
            )
        return redirect("/")

    posts = Post.objects.all().order_by("-created_at")

    # Get IDs of posts liked by the current user
    liked_post_ids = Like.objects.filter(user=request.user, post__in=posts).values_list('post_id', flat=True)

    return render(request, "feed/home.html", {
        "posts": posts,
        "liked_post_ids": liked_post_ids
    })


@login_required
def like_post(request, post_id):
    """
    Toggle like/unlike for a post from the homepage.
    """
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(user=request.user, post=post, comment=None).first()

    if like:
        like.delete()  # Unlike
    else:
        Like.objects.create(user=request.user, post=post, comment=None)
        KarmaTransaction.objects.create(user=post.author, points=5)

    return redirect("/")
