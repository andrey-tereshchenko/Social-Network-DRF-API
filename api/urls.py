from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'posts', views.PostViewSet, basename='posts')
router.register(r'likes', views.PostLikeViewSet, basename='likes')

urlpatterns = [
    path('', include(router.urls)),
    path('like/<int:pk>/', views.PostLikeView.as_view()),
    path('analytic/', views.AnalyticsAPIView.as_view()),
    path('user-activity/<int:user_id>/', views.UserActivityAPIView.as_view())
]
