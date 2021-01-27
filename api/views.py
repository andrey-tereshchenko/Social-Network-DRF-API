from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.models import User, Post, Like
from api.permissions import IsOwnerOrAdmin
from api.serializers import UserSerializer, PostSerializer, LikeSerializer, PostLikeSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['destroy', 'update', 'partial_update']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]


class PostLikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]


class PostLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        data = {}
        if request.user.is_authenticated:
            data['user_id'] = request.user.id
            serializer = PostLikeSerializer(instance=post, data=data, partial=True)
            if serializer.is_valid():
                liked_post = serializer.save()
            else:
                return Response(serializer.errors)
            if request.user in liked_post.likes.all():
                like_str = 'like'
            else:
                like_str = 'unlike'
            return Response({"success": "Post {} {} by {}".format(liked_post.title, like_str, request.user)},
                            status=status.HTTP_201_CREATED)
        else:
            return Response("User auth error", status=status.HTTP_401_UNAUTHORIZED)


class AnalyticsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        date_from = request.GET.get('date_from', '2020-01-01')
        date_to = request.GET.get('date_to', '2022-01-01')
        likes_analytic = Like.objects.filter(creation_date__range=[date_from, date_to]).values(
            'creation_date').annotate(
            count=Count('id'))
        return Response(likes_analytic)


class UserActivityAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if user:
            data = dict()
            data['user_name'] = user.username
            data['last_login'] = user.last_login
            data['last_request'] = user.last_request
            return Response(data)
        else:
            return Response({'Error': 'user with id={} does not exist'.format(user_id)},
                            status=status.HTTP_404_NOT_FOUND)
