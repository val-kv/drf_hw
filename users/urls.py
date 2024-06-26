from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserViewSet, UserCreateAPIView, UserListAPIView, UserLRetrieveAPIView, UserUpdateAPIView, \
    UserDestroyAPIView, PaymentsListAPIView

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('users/create/', UserCreateAPIView.as_view(), name='create_user'),
    path('users/', UserListAPIView.as_view(), name='user_list'),
    path('users/<str:email>/', UserLRetrieveAPIView.as_view(), name='user_detail'),
    path('users/update/<str:email>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('users/delete/<str:email>/', UserDestroyAPIView.as_view(), name='user_delete'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
