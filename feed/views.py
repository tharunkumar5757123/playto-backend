from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from .models import Post, Comment, Like, KarmaTransaction
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import render

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer

    @action(detail=True, methods=["POST"])
    def like(self, request, pk=None):
        user = request.user
        post = self.get_object()

        with transaction.atomic():
            like, created = Like.objects.get_or_create(user=user, post=post, comment=None)
            if not created:
                return Response({"detail": "Already liked"}, status=400)
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
            like, created = Like.objects.get_or_create(user=user, post=None, comment=comment)
            if not created:
                return Response({"detail": "Already liked"}, status=400)
            KarmaTransaction.objects.create(user=comment.author, points=1)
        return Response({"detail": "Comment liked"})

from rest_framework.views import APIView

class LeaderboardView(APIView):
    def get(self, request):
        since = timezone.now() - timezone.timedelta(hours=24)
        data = (KarmaTransaction.objects
                .filter(created_at__gte=since)
                .values("user__username")
                .annotate(points_sum=Sum("points"))
                .order_by("-points_sum")[:5])
        return Response(data)


def home(request):
    posts = Post.objects.all().order_by("-created_at")[:10]  # get latest 10 posts
    return render(request, "feed/home.html", {"posts": posts})