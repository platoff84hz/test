from django.contrib import admin

from .models import Direction, Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'academic_title', 'user')
    list_filter = ('position',)
    search_fields = ('full_name', 'position', 'academic_title')
    filter_horizontal = ('directions',)


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('qualification', 'code', 'name', 'profile')
    list_filter = ('qualification',)
    search_fields = ('qualification', 'code', 'name', 'profile')

# Register your models here.
