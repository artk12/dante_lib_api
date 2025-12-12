from django.core.management.base import BaseCommand
from django.db import transaction
from content import models
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Seed all grades, subjects, lessons, chapters and parts from folder structure'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create grades
            grades_data = [
                ('10', 'Grade 10'),
                ('12', 'Grade 12'),
                ('13', 'Grade 13'),
            ]
            grades = {}
            for code, name in grades_data:
                g, _ = models.Grade.objects.get_or_create(code=code, defaults={'name': name})
                grades[code] = g
            self.stdout.write(self.style.SUCCESS('✓ Grades created'))

            # Create subjects
            subjects_data = [
                ('biology1', 'Biology 1', 'fa'),
                ('arabic1', 'Arabic 1', 'fa'),
            ]
            subjects = {}
            for code, title, lang in subjects_data:
                s, _ = models.Subject.objects.get_or_create(
                    code=code,
                    defaults={'title': title, 'language': lang}
                )
                subjects[code] = s
            self.stdout.write(self.style.SUCCESS('✓ Subjects created'))

            # ===== GRADE 10 - BIOLOGY 1 =====
            lesson_bio_10, _ = models.Lesson.objects.get_or_create(
                grade=grades['10'],
                subject=subjects['biology1'],
                defaults={
                    'title': 'Biology 1 - Grade 10',
                    'description': 'Introduction to biology, living organisms, and biological molecules'
                }
            )

            # Chapter 1 - دنیای زنده
            chapter_10_bio_1, _ = models.Chapter.objects.get_or_create(
                lesson=lesson_bio_10,
                number=1,
                defaults={
                    'title': 'فصل 1 — دنیای زنده',
                    'summary': 'Introduction to biology, scope of life, and biological molecules'
                }
            )

            # Parts for Chapter 1
            parts_ch1 = [
                {
                    'number': 1,
                    'title': 'Part 1: گفتار 1 — زیستشناسی چیست؟',
                    'content_url': '/static/10/Biology_1/Chapter%201/Part%201/Bio1CH1P1C1.html',
                },
                {
                    'number': 2,
                    'title': 'Part 2: گفتار 2 — گستره حیات',
                    'content_url': '/static/10/Biology_1/Chapter%201/Part%202/Bio1CH1P2C1.html',
                },
                {
                    'number': 3,
                    'title': 'Part 3: گفتار 3 — یاخته و بافت',
                    'content_url': '/static/10/Biology_1/Chapter%201/Part%203/Bio1CH1P3C1.html',
                },
            ]
            for part_data in parts_ch1:
                models.Part.objects.get_or_create(
                    chapter=chapter_10_bio_1,
                    number=part_data['number'],
                    defaults={
                        'title': part_data['title'],
                        'content_type': 'url',
                        'content_url': part_data['content_url'],
                        'mime': 'text/html',
                    }
                )

            # Chapter 2 - سامانه های زنده
            chapter_10_bio_2, _ = models.Chapter.objects.get_or_create(
                lesson=lesson_bio_10,
                number=2,
                defaults={
                    'title': 'فصل 2 — سامانه‌های زنده',
                    'summary': 'Understanding living systems and their organization'
                }
            )

            parts_ch2 = [
                {
                    'number': 1,
                    'title': 'Part 1: گفتار 1',
                    'content_url': '/static/10/Biology_1/Chapter%202/Part%201/Bio1CH2P1C1.html',
                },
                {
                    'number': 2,
                    'title': 'Part 2: گفتار 2',
                    'content_url': '/static/10/Biology_1/Chapter%202/Part%202/Bio1CH2P2C1.html',
                },
            ]
            for part_data in parts_ch2:
                models.Part.objects.get_or_create(
                    chapter=chapter_10_bio_2,
                    number=part_data['number'],
                    defaults={
                        'title': part_data['title'],
                        'content_type': 'url',
                        'content_url': part_data['content_url'],
                        'mime': 'text/html',
                    }
                )

            self.stdout.write(self.style.SUCCESS('✓ Grade 10 Biology created (2 chapters, 5 parts)'))

            # ===== GRADE 10 - ARABIC 1 =====
            lesson_ar_10, _ = models.Lesson.objects.get_or_create(
                grade=grades['10'],
                subject=subjects['arabic1'],
                defaults={
                    'title': 'Arabic 1 - Grade 10',
                    'description': 'Arabic language fundamentals and grammar'
                }
            )

            chapter_10_ar_1, _ = models.Chapter.objects.get_or_create(
                lesson=lesson_ar_10,
                number=1,
                defaults={
                    'title': 'فصل 1 — اساسیات عربی',
                    'summary': 'Introduction to Arabic language'
                }
            )

            parts_ar_ch1 = [
                {
                    'number': 1,
                    'title': 'Part 1: درس 1 — الحروف',
                    'content_url': '/static/10/Arabic_1/Chapter%201/Part%201/Arabic1CH1P1.html',
                },
                {
                    'number': 2,
                    'title': 'Part 2: درس 2 — الكلمات',
                    'content_url': '/static/10/Arabic_1/Chapter%201/Part%202/Arabic1CH1P2.html',
                },
            ]
            for part_data in parts_ar_ch1:
                models.Part.objects.get_or_create(
                    chapter=chapter_10_ar_1,
                    number=part_data['number'],
                    defaults={
                        'title': part_data['title'],
                        'content_type': 'url',
                        'content_url': part_data['content_url'],
                        'mime': 'text/html',
                    }
                )

            self.stdout.write(self.style.SUCCESS('✓ Grade 10 Arabic created (1 chapter, 2 parts)'))

            # ===== GRADE 12 - BIOLOGY 1 =====
            lesson_bio_12, _ = models.Lesson.objects.get_or_create(
                grade=grades['12'],
                subject=subjects['biology1'],
                defaults={
                    'title': 'Biology 1 - Grade 12',
                    'description': 'Advanced biology topics: genetics and evolution'
                }
            )

            # Chapter 1 - ژنتیک
            chapter_12_bio_1, _ = models.Chapter.objects.get_or_create(
                lesson=lesson_bio_12,
                number=1,
                defaults={
                    'title': 'فصل 1 — ژنتیک و توارث',
                    'summary': 'Genetics and heredity'
                }
            )

            parts_12_bio_ch1 = [
                {
                    'number': 1,
                    'title': 'Part 1: ژن‌ها و انتقال صفات',
                    'content_url': '/static/12/Biology_1/Chapter%201/Part%201/Bio1CH1P1.html',
                },
                {
                    'number': 2,
                    'title': 'Part 2: انتقال ژن‌ها',
                    'content_url': '/static/12/Biology_1/Chapter%201/Part%202/Bio1CH1P2.html',
                },
                {
                    'number': 3,
                    'title': 'Part 3: محاسبات ژنتیکی',
                    'content_url': '/static/12/Biology_1/Chapter%201/Part%203/Bio1CH1P3.html',
                },
            ]
            for part_data in parts_12_bio_ch1:
                models.Part.objects.get_or_create(
                    chapter=chapter_12_bio_1,
                    number=part_data['number'],
                    defaults={
                        'title': part_data['title'],
                        'content_type': 'url',
                        'content_url': part_data['content_url'],
                        'mime': 'text/html',
                    }
                )

            # Chapter 2 - تکامل
            chapter_12_bio_2, _ = models.Chapter.objects.get_or_create(
                lesson=lesson_bio_12,
                number=2,
                defaults={
                    'title': 'فصل 2 — تکامل و انتخاب طبیعی',
                    'summary': 'Evolution and natural selection'
                }
            )

            parts_12_bio_ch2 = [
                {
                    'number': 1,
                    'title': 'Part 1: داروین و تکامل',
                    'content_url': '/static/12/Biology_1/Chapter%202/Part%201/Bio1CH2P1.html',
                },
                {
                    'number': 2,
                    'title': 'Part 2: شواهد تکامل',
                    'content_url': '/static/12/Biology_1/Chapter%202/Part%202/Bio1CH2P2.html',
                },
            ]
            for part_data in parts_12_bio_ch2:
                models.Part.objects.get_or_create(
                    chapter=chapter_12_bio_2,
                    number=part_data['number'],
                    defaults={
                        'title': part_data['title'],
                        'content_type': 'url',
                        'content_url': part_data['content_url'],
                        'mime': 'text/html',
                    }
                )

            self.stdout.write(self.style.SUCCESS('✓ Grade 12 Biology created (2 chapters, 5 parts)'))

            # ===== GRADE 12 - ARABIC 1 =====
            lesson_ar_12, _ = models.Lesson.objects.get_or_create(
                grade=grades['12'],
                subject=subjects['arabic1'],
                defaults={
                    'title': 'Arabic 1 - Grade 12',
                    'description': 'Advanced Arabic grammar and literature'
                }
            )

            chapter_12_ar_1, _ = models.Chapter.objects.get_or_create(
                lesson=lesson_ar_12,
                number=1,
                defaults={
                    'title': 'فصل 1 — النحو المتقدم',
                    'summary': 'Advanced Arabic grammar'
                }
            )

            parts_12_ar_ch1 = [
                {
                    'number': 1,
                    'title': 'Part 1: الجملة الفعلية',
                    'content_url': '/static/12/Arabic_1/Chapter%201/Part%201/Arabic1CH1P1.html',
                },
                {
                    'number': 2,
                    'title': 'Part 2: الجملة الاسمية',
                    'content_url': '/static/12/Arabic_1/Chapter%201/Part%202/Arabic1CH1P2.html',
                },
            ]
            for part_data in parts_12_ar_ch1:
                models.Part.objects.get_or_create(
                    chapter=chapter_12_ar_1,
                    number=part_data['number'],
                    defaults={
                        'title': part_data['title'],
                        'content_type': 'url',
                        'content_url': part_data['content_url'],
                        'mime': 'text/html',
                    }
                )

            self.stdout.write(self.style.SUCCESS('✓ Grade 12 Arabic created (1 chapter, 2 parts)'))

            # ===== GRADE 13 - BIOLOGY 1 =====
            lesson_bio_13, _ = models.Lesson.objects.get_or_create(
                grade=grades['13'],
                subject=subjects['biology1'],
                defaults={
                    'title': 'Biology 1 - Grade 13',
                    'description': 'Advanced biology: molecular biology and biotechnology'
                }
            )

            # Chapter 1 - بیولوژی مولکولی
            chapter_13_bio_1, _ = models.Chapter.objects.get_or_create(
                lesson=lesson_bio_13,
                number=1,
                defaults={
                    'title': 'فصل 1 — بیولوژی مولکولی',
                    'summary': 'Molecular biology and DNA'
                }
            )

            parts_13_bio_ch1 = [
                {
                    'number': 1,
                    'title': 'Part 1: ساختار DNA',
                    'content_url': '/static/13/Biology_1/Chapter%201/Part%201/Bio1CH1P1.html',
                },
                {
                    'number': 2,
                    'title': 'Part 2: تکثیر DNA',
                    'content_url': '/static/13/Biology_1/Chapter%201/Part%202/Bio1CH1P2.html',
                },
                {
                    'number': 3,
                    'title': 'Part 3: بیان ژن',
                    'content_url': '/static/13/Biology_1/Chapter%201/Part%203/Bio1CH1P3.html',
                },
            ]
            for part_data in parts_13_bio_ch1:
                models.Part.objects.get_or_create(
                    chapter=chapter_13_bio_1,
                    number=part_data['number'],
                    defaults={
                        'title': part_data['title'],
                        'content_type': 'url',
                        'content_url': part_data['content_url'],
                        'mime': 'text/html',
                    }
                )

            # Chapter 2 - بیوتکنولوژی
            chapter_13_bio_2, _ = models.Chapter.objects.get_or_create(
                lesson=lesson_bio_13,
                number=2,
                defaults={
                    'title': 'فصل 2 — بیوتکنولوژی و مهندسی ژنتیک',
                    'summary': 'Biotechnology and genetic engineering'
                }
            )

            parts_13_bio_ch2 = [
                {
                    'number': 1,
                    'title': 'Part 1: مهندسی ژنتیک',
                    'content_url': '/static/13/Biology_1/Chapter%202/Part%201/Bio1CH2P1.html',
                },
                {
                    'number': 2,
                    'title': 'Part 2: کاربردهای بیوتکنولوژی',
                    'content_url': '/static/13/Biology_1/Chapter%202/Part%202/Bio1CH2P2.html',
                },
            ]
            for part_data in parts_13_bio_ch2:
                models.Part.objects.get_or_create(
                    chapter=chapter_13_bio_2,
                    number=part_data['number'],
                    defaults={
                        'title': part_data['title'],
                        'content_type': 'url',
                        'content_url': part_data['content_url'],
                        'mime': 'text/html',
                    }
                )

            self.stdout.write(self.style.SUCCESS('✓ Grade 13 Biology created (2 chapters, 5 parts)'))

            # ===== GRADE 13 - ARABIC 1 =====
            lesson_ar_13, _ = models.Lesson.objects.get_or_create(
                grade=grades['13'],
                subject=subjects['arabic1'],
                defaults={
                    'title': 'Arabic 1 - Grade 13',
                    'description': 'Advanced Arabic literature and criticism'
                }
            )

            chapter_13_ar_1, _ = models.Chapter.objects.get_or_create(
                lesson=lesson_ar_13,
                number=1,
                defaults={
                    'title': 'فصل 1 — الأدب العربي',
                    'summary': 'Arabic literature and poetry'
                }
            )

            parts_13_ar_ch1 = [
                {
                    'number': 1,
                    'title': 'Part 1: الشعر العربي',
                    'content_url': '/static/13/Arabic_1/Chapter%201/Part%201/Arabic1CH1P1.html',
                },
                {
                    'number': 2,
                    'title': 'Part 2: النثر العربي',
                    'content_url': '/static/13/Arabic_1/Chapter%201/Part%202/Arabic1CH1P2.html',
                },
            ]
            for part_data in parts_13_ar_ch1:
                models.Part.objects.get_or_create(
                    chapter=chapter_13_ar_1,
                    number=part_data['number'],
                    defaults={
                        'title': part_data['title'],
                        'content_type': 'url',
                        'content_url': part_data['content_url'],
                        'mime': 'text/html',
                    }
                )

            self.stdout.write(self.style.SUCCESS('✓ Grade 13 Arabic created (1 chapter, 2 parts)'))

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                '\n' + '='*60 + '\n'
                '✅ ALL CONTENT SEEDED SUCCESSFULLY!\n'
                '='*60 + '\n'
                'GRADES: 10, 12, 13\n'
                'SUBJECTS: Biology 1, Arabic 1\n\n'
                'SUMMARY:\n'
                '  • Grade 10: 2 subjects × 1 lesson = 2 lessons (3 chapters, 7 parts)\n'
                '  • Grade 12: 2 subjects × 1 lesson = 2 lessons (3 chapters, 7 parts)\n'
                '  • Grade 13: 2 subjects × 1 lesson = 2 lessons (3 chapters, 7 parts)\n\n'
                '  TOTAL: 6 lessons, 9 chapters, 21 parts\n'
                '='*60
            )
        )