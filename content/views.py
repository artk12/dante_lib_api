from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from . import models, serializers
from .mixins import MessageResponseMixin
from rest_framework.views import APIView


class GradeListAPIView(MessageResponseMixin, generics.ListAPIView):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer
    message = 'grade find success'


class LessonsByGradeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        grade_id = request.data.get('grade_id')
        if not grade_id:
            raise ValidationError({'detail': 'grade_id is required'})

        lessons = models.Lesson.objects.filter(grade_id=grade_id)
        serializer = serializers.LessonSerializer(lessons, many=True)
        return Response({'message': 'lessons find success', 'data': serializer.data})


class ChaptersByLessonAPIView(generics.GenericAPIView):
    
    serializer_class = serializers.ChapterSerializer  # Serializer اصلی Chapter

    def post(self, request, *args, **kwargs):
        lesson_id = request.data.get('lesson_id')
        if not lesson_id:
            raise ValidationError({'detail': 'lesson_id is required'})

        chapters = models.Chapter.objects.filter(lesson_id=lesson_id).order_by('number')
        serializer = self.get_serializer(chapters, many=True)

        return Response(
            {
                "status_code": 200,
                "message": "OK",
                "data": serializer.data
            },
            status=200
        )



class PartsByChapterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        chapter_id = request.data.get('chapter_id')

        if not chapter_id:
            raise ValidationError({'detail': 'chapter_id is required'})

        parts = models.Part.objects.filter(chapter_id=chapter_id).order_by('number')

        serializer = serializers.PartSerializer(parts, many=True)

        return Response(
            {
                "status_code": 200,
                "message": "OK",
                "data": serializer.data
            },
            status=200
        )


class PartDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Part.objects.all()
    serializer_class = serializers.PartSerializer
