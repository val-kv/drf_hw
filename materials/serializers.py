from rest_framework import serializers
from materials.models import Course, Lesson, Subscribe
from materials.validators import validate_materials_link


class SubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = ['is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscribe.objects.filter(user=user, course=obj.course).exists()


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [validate_materials_link]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    subscribe = SubscribeSerializer(many=True, read_only=True)
    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lesson_count', 'lessons']
