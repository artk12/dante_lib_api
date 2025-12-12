from django.urls import path
from . import views

urlpatterns = [
    path('grades', views.GradeListAPIView.as_view(), name='grades-list'),
    path('lessons', views.LessonsByGradeAPIView.as_view(), name='lessons-list'),
    path('grades/<uuid:grade_id>/lessons', views.LessonsByGradeAPIView.as_view(), name='lessons-by-grade'),
    path('chapters', views.ChaptersByLessonAPIView.as_view(), name='chapters-list'),
    path('lessons/<uuid:lesson_id>/chapters', views.ChaptersByLessonAPIView.as_view(), name='chapters-by-lesson'),
    path('parts', views.PartsByChapterAPIView.as_view(), name='parts-list'),
    path('chapters/<uuid:chapter_id>/parts', views.PartsByChapterAPIView.as_view(), name='parts-by-chapter'),
    path('parts/<uuid:pk>', views.PartDetailAPIView.as_view(), name='part-detail'),
]
