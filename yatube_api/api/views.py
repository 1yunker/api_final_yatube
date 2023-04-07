from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Group, Post
from .permissions import IsOwner
from .serializers import (
    GroupSerializer,
    PostSerializer,
    CommentSerializer,
)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        post_obj = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post_obj.comments

    def perform_create(self, serializer):
        post_obj = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user,
                        post=post_obj)
