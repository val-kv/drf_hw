from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='materials/media', null=True, blank=True)
    description = models.TextField()
    lesson_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='materials/media', null=True, blank=True)
    description = models.TextField()
    video = models.FileField(upload_to='materials/media', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
