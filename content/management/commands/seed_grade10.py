from pathlib import Path
import re
from urllib.parse import quote
from datetime import datetime
from typing import Optional
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from content import models

GRADE_PATH = Path("/Users/artk/Downloads/content html 2/10")


def normalize_subject_code(name: str) -> str:
    s = re.sub(r"[^0-9A-Za-z]+", "_", name).lower()
    s = re.sub(r"_+", "_", s).strip("_")
    s = re.sub(r"_(\d+)$", r"\1", s)
    return s


def extract_number(s: str) -> Optional[int]:
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else None


def quote_segments(*segments: str) -> str:
    return "/".join(quote(seg) for seg in segments)


class Command(BaseCommand):
    help = "Scan /Users/artk/Downloads/content html 2/10 and seed Grade 10 subjects/lessons/chapters/parts"

    def handle(self, *args, **options):
        if not GRADE_PATH.exists() or not GRADE_PATH.is_dir():
            self.stderr.write(f"Grade folder not found: {GRADE_PATH}")
            return

        counts = {"subjects": 0, "lessons": 0, "chapters": 0, "parts": 0}
        exists = {"subjects": 0, "lessons": 0, "chapters": 0, "parts": 0}

        with transaction.atomic():
            grade, _ = models.Grade.objects.get_or_create(code="10", defaults={"name": "Grade 10"})
            self.stdout.write(self.style.SUCCESS(f"Ensured grade: {grade.code}"))

            for subject_dir in sorted(p for p in GRADE_PATH.iterdir() if p.is_dir()):
                subj_code = normalize_subject_code(subject_dir.name)
                subj_title = subject_dir.name.replace("_", " ").strip()
                subject, created = models.Subject.objects.get_or_create(
                    code=subj_code, defaults={"title": subj_title, "language": "fa"}
                )
                if created:
                    counts["subjects"] += 1
                    self.stdout.write(f"Created subject: {subject.code}")
                else:
                    exists["subjects"] += 1
                    self.stdout.write(f"Subject exists: {subject.code}")

                lesson_title = f"{subject.title} - Grade 10"
                lesson, l_created = models.Lesson.objects.get_or_create(
                    grade=grade, subject=subject, defaults={"title": lesson_title, "description": ""}
                )
                if l_created:
                    counts["lessons"] += 1
                else:
                    exists["lessons"] += 1

                # iterate chapter folders or files under subject_dir
                for chapter_dir in sorted(subject_dir.iterdir()):
                    if chapter_dir.is_dir():
                        chap_num = extract_number(chapter_dir.name) or 0
                        chap_title = chapter_dir.name.replace("_", " ").strip()
                        chapter, c_created = models.Chapter.objects.get_or_create(
                            lesson=lesson, number=chap_num, defaults={"title": chap_title, "summary": ""}
                        )
                        if c_created:
                            counts["chapters"] += 1
                        else:
                            exists["chapters"] += 1

                        # check for part subfolders
                        part_dirs = [p for p in chapter_dir.iterdir() if p.is_dir()]
                        if part_dirs:
                            for pd in sorted(part_dirs):
                                part_num = extract_number(pd.name) or 0
                                html_files = [f for f in sorted(pd.iterdir()) if f.is_file() and f.suffix.lower() == ".html"]
                                if not html_files:
                                    rel_url = "/static/" + quote_segments("10", subject_dir.name, chapter_dir.name, pd.name) + "/"
                                    defaults = {
                                        "title": pd.name,
                                        "content_type": "url",
                                        "content_url": rel_url,
                                        "mime": "text/html",
                                    }
                                    part_obj, p_created = models.Part.objects.get_or_create(
                                        chapter=chapter, number=part_num or 1, defaults=defaults
                                    )
                                    if p_created:
                                        counts["parts"] += 1
                                    else:
                                        exists["parts"] += 1
                                    continue

                                for idx, hf in enumerate(html_files):
                                    num = part_num + idx if len(html_files) > 1 else (part_num or 1)
                                    rel_url = "/static/" + quote_segments("10", subject_dir.name, chapter_dir.name, pd.name, hf.name)
                                    stat = hf.stat()
                                    defaults = {
                                        "title": hf.stem,
                                        "content_type": "url",
                                        "content_url": rel_url,
                                        "mime": "text/html",
                                    }
                                    if hasattr(models.Part, "size_bytes"):
                                        defaults["size_bytes"] = stat.st_size
                                    if hasattr(models.Part, "last_modified"):
                                        defaults["last_modified"] = datetime.fromtimestamp(stat.st_mtime, tz=timezone.get_default_timezone())
                                    base_num = num
                                    while True:
                                        if not models.Part.objects.filter(chapter=chapter, number=num).exists():
                                            part_obj, p_created = models.Part.objects.get_or_create(
                                                chapter=chapter, number=num, defaults=defaults
                                            )
                                            if p_created:
                                                counts["parts"] += 1
                                            else:
                                                exists["parts"] += 1
                                            break
                                        num += 1
                                        if num > base_num + 1000:
                                            break
                        else:
                            # treat html files in chapter_dir as parts
                            html_files = [f for f in sorted(chapter_dir.iterdir()) if f.is_file() and f.suffix.lower() == ".html"]
                            for idx, hf in enumerate(html_files, start=1):
                                rel_url = "/static/" + quote_segments("10", subject_dir.name, chapter_dir.name, hf.name)
                                stat = hf.stat()
                                defaults = {
                                    "title": hf.stem,
                                    "content_type": "url",
                                    "content_url": rel_url,
                                    "mime": "text/html",
                                }
                                if hasattr(models.Part, "size_bytes"):
                                    defaults["size_bytes"] = stat.st_size
                                if hasattr(models.Part, "last_modified"):
                                    defaults["last_modified"] = datetime.fromtimestamp(stat.st_mtime, tz=timezone.get_default_timezone())
                                num = idx
                                base_num = num
                                while True:
                                    if not models.Part.objects.filter(chapter=chapter, number=num).exists():
                                        part_obj, p_created = models.Part.objects.get_or_create(
                                            chapter=chapter, number=num, defaults=defaults
                                        )
                                        if p_created:
                                            counts["parts"] += 1
                                        else:
                                            exists["parts"] += 1
                                        break
                                    num += 1
                                    if num > base_num + 1000:
                                        break
                    else:
                        # if there are html files directly under subject (no Chapter folders), create a default chapter 1
                        if chapter_dir.suffix.lower() == ".html":
                            chapter, c_created = models.Chapter.objects.get_or_create(
                                lesson=lesson, number=1, defaults={"title": "Chapter 1", "summary": ""}
                            )
                            if c_created:
                                counts["chapters"] += 1
                            else:
                                exists["chapters"] += 1
                            hf = chapter_dir
                            rel_url = "/static/" + quote_segments("10", subject_dir.name, hf.name)
                            stat = hf.stat()
                            defaults = {
                                "title": hf.stem,
                                "content_type": "url",
                                "content_url": rel_url,
                                "mime": "text/html",
                            }
                            if hasattr(models.Part, "size_bytes"):
                                defaults["size_bytes"] = stat.st_size
                            if hasattr(models.Part, "last_modified"):
                                defaults["last_modified"] = datetime.fromtimestamp(stat.st_mtime, tz=timezone.get_default_timezone())
                            if not models.Part.objects.filter(chapter=chapter, number=1).exists():
                                models.Part.objects.create(chapter=chapter, number=1, **defaults)
                                counts["parts"] += 1
                            else:
                                exists["parts"] += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nSeed complete for Grade 10\n"
            f"Subjects created: {counts['subjects']}  (exists: {exists['subjects']})\n"
            f"Lessons created: {counts['lessons']}   (exists: {exists['lessons']})\n"
            f"Chapters created: {counts['chapters']}  (exists: {exists['chapters']})\n"
            f"Parts created: {counts['parts']}     (exists: {exists['parts']})\n"
            f"Run: python manage.py seed_grade10\n"
        ))
