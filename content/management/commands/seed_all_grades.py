from pathlib import Path
import re
from urllib.parse import quote
from datetime import datetime
from typing import Optional
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from content import models


# =====================
# Utils
# =====================

def normalize_code(name: str) -> str:
    s = re.sub(r"[^0-9A-Za-z]+", "_", name).lower()
    s = re.sub(r"_+", "_", s).strip("_")
    return s


def extract_number(s: str) -> Optional[int]:
    match = re.search(r"(\d+)", s)
    return int(match.group(1)) if match else None


def quote_segments(*segments: str) -> str:
    return "/".join(quote(seg) for seg in segments)


def find_html_files(path: Path):
    return [p for p in sorted(path.iterdir()) if p.is_file() and p.suffix.lower() == ".html"]


# =====================
# Core Scanner
# =====================

class GradeScanner:

    def __init__(self, root: Path, stdout):
        self.root = root
        self.stdout = stdout

    def scan_all_grades(self):
        """Find folders whose names are numeric → treat each as a grade."""
        grade_dirs = [d for d in self.root.iterdir() if d.is_dir() and d.name.isdigit()]

        if not grade_dirs:
            self.stdout.write("No grade directories found.")
            return

        for gd in sorted(grade_dirs, key=lambda x: int(x.name)):
            grade_code = gd.name
            self.scan_grade(grade_code, gd)

    def scan_grade(self, grade_code: str, grade_path: Path):
        with transaction.atomic():

            grade, _ = models.Grade.objects.get_or_create(
                code=grade_code,
                defaults={"name": f"Grade {grade_code}"}
            )

            self.stdout.write(f"\n=== Scanning Grade {grade_code} ===")

            for subject_dir in sorted(grade_path.iterdir()):
                if subject_dir.is_dir():
                    self.scan_subject(grade, subject_dir)

    def scan_subject(self, grade, subject_dir: Path):
        subj_code = normalize_code(subject_dir.name)
        subj_title = subject_dir.name.replace("_", " ").strip()

        subject, _ = models.Subject.objects.get_or_create(
            code=subj_code,
            defaults={"title": subj_title, "language": "fa"}
        )

        lesson_title = f"{subject.title} - Grade {grade.code}"

        lesson, _ = models.Lesson.objects.get_or_create(
            grade=grade,
            subject=subject,
            defaults={"title": lesson_title, "description": ""}
        )

        for item in sorted(subject_dir.iterdir()):
            if item.is_dir():
                self.scan_chapter(lesson, item, grade.code, subject_dir.name)
            elif item.suffix.lower() == ".html":
                # subject has HTML directly → a default chapter
                self.scan_default_chapter_file(lesson, item, grade.code, subject_dir.name)

    def scan_chapter(self, lesson, chapter_dir: Path, grade_code: str, subject_name: str):
        chap_num = extract_number(chapter_dir.name) or 1
        chap_title = chapter_dir.name.replace("_", " ").strip()

        chapter, _ = models.Chapter.objects.get_or_create(
            lesson=lesson,
            number=chap_num,
            defaults={"title": chap_title, "summary": ""}
        )

        part_dirs = [p for p in chapter_dir.iterdir() if p.is_dir()]

        if part_dirs:
            for pd in sorted(part_dirs):
                self.scan_part_dir(chapter, pd, grade_code, subject_name, chapter_dir.name)
        else:
            self.scan_html_in_chapter_root(chapter, chapter_dir, grade_code, subject_name)

    def scan_part_dir(self, chapter, part_dir: Path, grade_code: str, subject_name: str, chapter_name: str):
        part_num = extract_number(part_dir.name) or 1
        html_files = find_html_files(part_dir)

        if not html_files:
            # no html → part itself links to directory
            rel_url = "/static/" + quote_segments(
                grade_code, subject_name, chapter_name, part_dir.name
            )

            models.Part.objects.get_or_create(
                chapter=chapter,
                number=part_num,
                defaults={
                    "title": part_dir.name,
                    "content_type": "url",
                    "content_url": rel_url,
                    "mime": "text/html",
                },
            )
            return

        for idx, hf in enumerate(html_files):
            num = part_num if len(html_files) == 1 else part_num + idx
            self.create_part_from_file(chapter, num, hf,
                                       grade_code, subject_name, chapter_name, part_dir.name)

    def scan_html_in_chapter_root(self, chapter, chapter_dir: Path, grade_code: str, subject_name: str):
        html_files = find_html_files(chapter_dir)

        for idx, hf in enumerate(html_files, start=1):
            self.create_part_from_file(chapter, idx, hf,
                                       grade_code, subject_name, chapter_dir.name)

    def scan_default_chapter_file(self, lesson, file: Path, grade_code: str, subject_name: str):
        chapter, _ = models.Chapter.objects.get_or_create(
            lesson=lesson,
            number=1,
            defaults={"title": "Chapter 1", "summary": ""}
        )
        self.create_part_from_file(chapter, 1, file,
                                   grade_code, subject_name, "")

    def create_part_from_file(self, chapter, number: int, file: Path,
                              grade_code: str, subject_name: str,
                              chapter_or_part_name: str = "",
                              part_dir_name: str = ""):

        segments = [grade_code, subject_name]
        if chapter_or_part_name:
            segments.append(chapter_or_part_name)
        if part_dir_name:
            segments.append(part_dir_name)
        segments.append(file.name)

        rel_url = "/static/" + quote_segments(*segments)

        stat = file.stat()

        defaults = {
            "title": file.stem,
            "content_type": "url",
            "content_url": rel_url,
            "mime": "text/html",
        }

        if hasattr(models.Part, "size_bytes"):
            defaults["size_bytes"] = stat.st_size

        if hasattr(models.Part, "last_modified"):
            defaults["last_modified"] = datetime.fromtimestamp(
                stat.st_mtime, tz=timezone.get_default_timezone()
            )

        models.Part.objects.get_or_create(
            chapter=chapter,
            number=number,
            defaults=defaults
        )


# =====================
# Django Command
# =====================

class Command(BaseCommand):
    help = "Automatically scan all numeric grade folders and seed DB."

    def add_arguments(self, parser):
        parser.add_argument(
            "--root",
            required=True,
            help="Root directory containing grade folders (e.g. /path/to/content)"
        )

    def handle(self, *args, **options):
        root = Path(options["root"])

        if not root.exists():
            self.stderr.write(f"Root directory not found: {root}")
            return

        scanner = GradeScanner(root, stdout=self.stdout)
        scanner.scan_all_grades()

        self.stdout.write("\nSeeding complete for all grades.")
