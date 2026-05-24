from django.conf import settings
from django.db import models
from django.urls import reverse


class Direction(models.Model):
    qualification = models.CharField('Квалификация', max_length=80)
    code = models.CharField('Код направления', max_length=20, blank=True)
    name = models.CharField('Направление', max_length=180)
    profile = models.CharField('Профиль', max_length=220)

    class Meta:
        ordering = ['qualification', 'code', 'name', 'profile']
        verbose_name = 'направление подготовки'
        verbose_name_plural = 'направления подготовки'

    def __str__(self):
        prefix = f'{self.code} ' if self.code else ''
        return f'{self.qualification}: {prefix}{self.name} - {self.profile}'

    def get_absolute_url(self):
        return reverse('directions')


class Teacher(models.Model):
    POSITION_HEAD = 'Заведующий кафедрой'
    POSITION_PROFESSOR = 'Профессор'
    POSITION_DOCENT = 'Доцент'
    POSITION_SENIOR = 'Старший преподаватель'

    POSITION_CHOICES = [
        (POSITION_HEAD, POSITION_HEAD),
        (POSITION_PROFESSOR, POSITION_PROFESSOR),
        (POSITION_DOCENT, POSITION_DOCENT),
        (POSITION_SENIOR, POSITION_SENIOR),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name='Учетная запись',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='teacher_profile',
    )
    full_name = models.CharField('ФИО', max_length=180)
    position = models.CharField('Должность', max_length=80, choices=POSITION_CHOICES)
    academic_title = models.CharField('Ученое звание', max_length=120, blank=True)
    photo_url = models.URLField('URL фотографии', blank=True)
    directions = models.ManyToManyField(Direction, verbose_name='Направления подготовки', blank=True)
    bio = models.TextField('Краткая информация', blank=True)

    class Meta:
        ordering = ['full_name']
        verbose_name = 'преподаватель'
        verbose_name_plural = 'преподаватели'

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('teachers')

# Create your models here.
class Subject(models.Model):
    """Модель дисциплины/предмета"""
    name = models.CharField('Название дисциплины', max_length=200)
    code = models.CharField('Код дисциплины', max_length=20, blank=True)
    hours = models.PositiveIntegerField('Часов', default=72)
    semester = models.PositiveSmallIntegerField('Семестр', default=1)
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects',
        verbose_name='Преподаватель'
    )
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        ordering = ['semester', 'name']
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'
    
    def __str__(self):
        return f"{self.name} ({self.semester} семестр)"