from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import Direction, Teacher, Subject


class Command(BaseCommand):
    help = 'Creates demo users, teachers and education directions for the department site.'

    def handle(self, *args, **options):
        User = get_user_model()

        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'},
        )
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password('admin123')
        admin.save()

        teacher_user, _ = User.objects.get_or_create(
            username='teacher',
            defaults={'first_name': 'Преподаватель'},
        )
        teacher_user.set_password('teacher123')
        teacher_user.save()

        directions_data = [
            ('Бакалавриат', '09.03.03', 'Прикладная информатика', 'Информационные системы и технологии'),
            ('Бакалавриат', '09.03.04', 'Программная инженерия', 'Разработка программно-информационных систем'),
            ('Магистратура', '09.04.03', 'Прикладная информатика', 'Информационные системы в экономике и управлении'),
            ('Магистратура', '09.04.04', 'Программная инженерия', 'Управление разработкой программных проектов'),
            ('Специалитет', '10.05.03', 'Информационная безопасность автоматизированных систем', 'Безопасность открытых информационных систем'),
            ('Бакалавриат', '38.03.05', 'Бизнес-информатика', 'Цифровая трансформация бизнеса'),
            ('Магистратура', '38.04.05', 'Бизнес-информатика', 'Архитектура предприятия и ИТ-консалтинг'),
            ('Бакалавриат', '02.03.03', 'Математическое обеспечение и администрирование информационных систем', 'Технологии программирования'),
            ('Магистратура', '02.04.03', 'Математическое обеспечение и администрирование информационных систем', 'Интеллектуальный анализ данных'),
            ('Специалитет', '09.05.01', 'Применение и эксплуатация автоматизированных систем специального назначения', 'Информационно-аналитические системы'),
            ('Бакалавриат', '27.03.03', 'Системный анализ и управление', 'Информационные технологии управления'),
            ('Магистратура', '27.04.03', 'Системный анализ и управление', 'Управление сложными информационными системами'),
        ]
        directions = []
        for qualification, code, name, profile in directions_data:
            direction, _ = Direction.objects.get_or_create(
                code=code,
                profile=profile,
                defaults={'qualification': qualification, 'name': name},
            )
            direction.qualification = qualification
            direction.name = name
            direction.save()
            directions.append(direction)

        teachers_data = [
            (teacher_user, 'Ярушкина Надежда Глебовна', Teacher.POSITION_HEAD, 'профессор, доктор технических наук', directions[:4]),
            (None, 'Варламова Светлана Анатольевна', Teacher.POSITION_PROFESSOR, 'профессор, доктор технических наук', directions[2:6]),
            (None, 'Гришин Александр Викторович', Teacher.POSITION_DOCENT, 'доцент, кандидат технических наук', directions[0:3]),
            (None, 'Кошкарев Александр Александрович', Teacher.POSITION_DOCENT, 'доцент, кандидат технических наук', directions[4:8]),
            (None, 'Майоров Николай Викторович', Teacher.POSITION_SENIOR, 'старший преподаватель', directions[1:5]),
            (None, 'Муратова Елена Александровна', Teacher.POSITION_DOCENT, 'доцент, кандидат технических наук', directions[6:10]),
            (None, 'Павлов Дмитрий Александрович', Teacher.POSITION_SENIOR, 'старший преподаватель', directions[8:12]),
        ]
            # Добавьте после создания преподавателей:
        teacher_obj = Teacher.objects.filter(user=teacher_user).first()

        subjects_data = [
            ('Базы данных', 'БД-101', 72, 3, teacher_obj),  # теперь передаем Teacher
            ('Web-программирование', 'WP-201', 108, 4, teacher_obj),
            ('Python для анализа данных', 'PD-301', 72, 5, None),  # None - без преподавателя
            ('Информационная безопасность', 'IB-401', 90, 6, None),
            ('Проектирование ИС', 'PIS-501', 108, 7, None),
        ]

        for name, code, hours, semester, teacher in subjects_data:
            Subject.objects.get_or_create(
                name=name,
                defaults={
                    'code': code,
                    'hours': hours,
                    'semester': semester,
                    'teacher': teacher  # teacher должен быть объектом Teacher или None
                }
            )
            
        for user, full_name, position, title, teacher_directions in teachers_data:
            teacher, _ = Teacher.objects.get_or_create(full_name=full_name)
            teacher.user = user
            teacher.position = position
            teacher.academic_title = title
            teacher.bio = 'Преподаватель кафедры информационных систем УлГТУ.'
            teacher.save()
            teacher.directions.set(teacher_directions)

        self.stdout.write(self.style.SUCCESS('Demo data created. Users: admin/admin123, teacher/teacher123.'))

