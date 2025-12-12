from django.contrib import admin
from . import models


@admin.register(models.Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'created_at')


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'title', 'language', 'created_at')


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'grade', 'subject', 'created_at')


@admin.register(models.Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'number', 'title', 'created_at')


@admin.register(models.Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('id', 'chapter', 'number', 'title', 'mime', 'content_type', 'created_at')
