from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import *
from .permissions import IsAuthorPermission
from .serializers import PostSerializer, ReplySerializer, CommentSerializer, LikeSerializer, RatingSerializer


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [permission() for permission in permissions]



class PostViewSet(PermissionMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # http_method_names = ['GET', 'POST', 'PUT', 'DELETE']


    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context['action'] = self.action
        return context



    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        print(request.query_params)
        q = request.query_params.get('q')  # request.query_params = request.GET
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(discription__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReplyViewSet(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get_serializer_context(self):
        context = super(ReplyViewSet, self).get_serializer_context()
        context['action'] = self.action
        return context


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class AddStarRatingView(ModelViewSet):
    """Добавление рейтинга посту"""

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer



class LikeViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet ):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    bad_request_message = 'An error has occurred'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context



    @action(detail=False, methods=['post'])
    def post(self, request):
        post = get_object_or_404(Post, slug=request.data.get('slug'))
        if request.user not in post.favourite.all():
            post.favourite.add(request.user)
            return Response({'detail': 'User added to post'}, status=status.HTTP_200_OK)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def delete(self, request):
        post = get_object_or_404(Post, slug=request.data.get('slug'))
        if request.user in post.favourite.all():
            post.favourite.remove(request.user)
            return Response({'detail': 'User removed from post'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)