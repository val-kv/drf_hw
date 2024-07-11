from django.shortcuts import render
from rest_framework import viewsets, generics, status
from materials.models import Course, Lesson, Subscribe
from materials.serializers import CourseSerializer, LessonSerializer
from users.models import Payments
from users.serializers import PaymentsSerializer
from .paginators import MaterialsPaginator
from .permissions import IsModeratorPermission, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from payment_integration import create_checkout_session, create_product, create_price
from materials.tasks import send_email_task


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated, IsModeratorPermission]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MaterialsPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModeratorPermission]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscribeView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = Course.objects.get_object_or_404(id=course_id)
        subs_item = Subscribe.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscribe.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

            # Send email to subscribed users
            subject = f'Обновление курса: {course.name}'
            message = f'Курс {course.name} был обновлен.'
            from_email = 'your_email@example.com'
            recipient_list = [sub.user.email for sub in Subscribe.objects.filter(course=course)]
            send_email_task.delay(subject, message, from_email, recipient_list)

        return Response({"message": message}, status=status.HTTP_200_OK)


def get_user_payments(request):
    user = request.user
    payments = Payments.objects.filter(user=user)
    serializer = PaymentsSerializer(payments, many=True)
    return serializer


def create_product_view(request):
    product_id = create_product()
    return render(request, 'product_created.html', {'product_id': product_id})


def create_price_view(request, product_id):
    price_id = create_price(product_id)
    return render(request, 'price_created.html', {'price_id': price_id})


def create_checkout_session_view(request, price_id):
    checkout_session_url = create_checkout_session(price_id)
    return render(request, 'checkout_session_created.html', {'checkout_session_url': checkout_session_url})