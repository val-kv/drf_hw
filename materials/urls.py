from django.urls import path
from rest_framework.routers import DefaultRouter

from materials import views, payment_integration
from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscribeView

app_name = 'materials'

router = DefaultRouter()
router.register(r'materials', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('create_product/', views.create_product_view, name='create_product'),
    path('create_price/<int:product_id>/', views.create_price_view, name='create_price'),
    path('create_checkout_session/<int:price_id>/', views.create_checkout_session_view, name='create_checkout_session'),
] + router.urls


def swagger_info():
    return {
        'description': 'API documentation for your_project',
        'title': 'Your Project API',
        'version': '1.0',
    }
