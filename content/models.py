import uuid
from django.db import models


class TimeStampedUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Grade(TimeStampedUUIDModel):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Subject(TimeStampedUUIDModel):
    code = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


class Lesson(TimeStampedUUIDModel):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='lessons')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = (('grade', 'subject'),)

    def __str__(self):
        return f"{self.title} ({self.grade.code} / {self.subject.code})"


class Chapter(TimeStampedUUIDModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='chapters')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)

    class Meta:
        unique_together = (('lesson', 'number'),)
        ordering = ['number']

    def __str__(self):
        return f"{self.lesson.title} - Chapter {self.number}: {self.title}"


class Part(TimeStampedUUIDModel):
    CONTENT_TYPE_URL = 'url'
    CONTENT_TYPE_INLINE = 'inline'
    CONTENT_TYPE_CHOICES = (
        (CONTENT_TYPE_URL, 'URL'),
        (CONTENT_TYPE_INLINE, 'Inline HTML'),
    )

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='parts')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    mime = models.CharField(max_length=128, default='text/html')
    content_type = models.CharField(max_length=16, choices=CONTENT_TYPE_CHOICES, default=CONTENT_TYPE_INLINE)
    content_url = models.CharField(max_length=1024, blank=True, null=True)
    html = models.TextField(blank=True)
    size_bytes = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('chapter', 'number'),)
        ordering = ['number']

    def __str__(self):
        return f"{self.chapter} - Part {self.number}: {self.title}"
