from rest_framework import serializers
from . import models


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Part
        fields = ['id', 'chapter', 'number', 'title', 'mime', 'content_type', 'content_url', 'html', 'size_bytes', 'created_at', 'updated_at']


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ['id', 'lesson', 'number', 'title', 'summary', 'created_at', 'updated_at']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ['id', 'grade', 'subject', 'title', 'description', 'created_at', 'updated_at']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ['id', 'code', 'title', 'language', 'created_at', 'updated_at']


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = ['id', 'code', 'name', 'created_at', 'updated_at']


# Create serializers
class LessonCreateSerializer(serializers.ModelSerializer):
    grade_id = serializers.UUIDField(write_only=True)
    subject_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = models.Lesson
        fields = ['id', 'grade_id', 'subject_id', 'title', 'description']


class ChapterCreateSerializer(serializers.ModelSerializer):
    lesson_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = models.Chapter
        fields = ['id', 'lesson_id', 'number', 'title', 'summary']


class PartCreateSerializer(serializers.ModelSerializer):
    chapter_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = models.Part
        fields = ['id', 'chapter_id', 'number', 'title', 'mime', 'content_type', 'content_url', 'html', 'size_bytes']
