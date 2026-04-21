"""
Management command to seed the database with sample data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from results.models import Department, StudentProfile, Subject, Result


class Command(BaseCommand):
    help = 'Seeds the database with sample departments, students, subjects and results'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Groups
        admin_group, _  = Group.objects.get_or_create(name='Admin')
        student_group, _ = Group.objects.get_or_create(name='Student')

        # Superuser / admin
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@srms.com', 'admin123')
            admin_user.first_name = 'System'
            admin_user.last_name  = 'Admin'
            admin_user.save()
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS('  Created admin user  →  admin / admin123'))

        # Departments
        dept_data = [
            ('Computer Science & Engineering (AI&ML)', 'CSE-AIML'),
            ('Computer Science & Engineering', 'CSE'),
            ('Electronics & Communication', 'ECE'),
            ('Mechanical Engineering', 'ME'),
        ]
        depts = {}
        for name, code in dept_data:
            d, _ = Department.objects.get_or_create(code=code, defaults={'name': name})
            depts[code] = d
        self.stdout.write(self.style.SUCCESS(f'  Created {len(depts)} departments'))

        # Subjects for CSE-AIML Sem 1 & 2
        subject_data = [
            ('Mathematics-I',              'MA101', 'CSE-AIML', 1, 100, 4),
            ('Physics',                    'PH101', 'CSE-AIML', 1, 100, 4),
            ('Programming in C',           'CS101', 'CSE-AIML', 1, 100, 4),
            ('Engineering Graphics',       'ME101', 'CSE-AIML', 1, 100, 2),
            ('Basic Electronics',          'EC101', 'CSE-AIML', 1, 100, 3),
            ('Mathematics-II',             'MA201', 'CSE-AIML', 2, 100, 4),
            ('Data Structures',            'CS201', 'CSE-AIML', 2, 100, 4),
            ('Digital Electronics',        'EC201', 'CSE-AIML', 2, 100, 3),
            ('Object Oriented Programming','CS202', 'CSE-AIML', 2, 100, 4),
            ('Discrete Mathematics',       'MA202', 'CSE-AIML', 2, 100, 3),
        ]
        subjects = {}
        for name, code, dept_code, sem, max_m, cred in subject_data:
            s, _ = Subject.objects.get_or_create(
                code=code,
                defaults={'name': name, 'department': depts[dept_code],
                          'semester': sem, 'max_marks': max_m, 'credits': cred}
            )
            subjects[code] = s
        self.stdout.write(self.style.SUCCESS(f'  Created {len(subjects)} subjects'))

        # Sample students
        student_data = [
            ('appaji',    'Appaji',  'Reddy',   '1DB22CI017', 'CSE-AIML', 2),
            ('student2',  'Priya',   'Sharma',  '1DB22CI018', 'CSE-AIML', 2),
            ('student3',  'Rahul',   'Kumar',   '1DB22CI019', 'CSE-AIML', 2),
        ]
        student_profiles = []
        for username, first, last, roll, dept_code, sem in student_data:
            if not User.objects.filter(username=username).exists():
                u = User.objects.create_user(username, f'{username}@srms.com', 'student123')
                u.first_name = first
                u.last_name  = last
                u.save()
                u.groups.add(student_group)
                p, _ = StudentProfile.objects.get_or_create(
                    roll_number=roll,
                    defaults={'user': u, 'department': depts[dept_code], 'current_semester': sem}
                )
                student_profiles.append(p)
                self.stdout.write(f'  Created student  →  {username} / student123')
            else:
                try:
                    student_profiles.append(StudentProfile.objects.get(roll_number=roll))
                except StudentProfile.DoesNotExist:
                    pass

        # Sample results
        admin_user = User.objects.get(username='admin')
        marks_map = {
            # (student_index, subject_code): marks
            (0, 'MA101'): 88, (0, 'PH101'): 74, (0, 'CS101'): 92,
            (0, 'ME101'): 65, (0, 'EC101'): 78,
            (0, 'MA201'): 82, (0, 'CS201'): 95, (0, 'EC201'): 70,
            (0, 'CS202'): 89, (0, 'MA202'): 76,
            (1, 'MA101'): 55, (1, 'PH101'): 62, (1, 'CS101'): 70,
            (1, 'ME101'): 45, (1, 'EC101'): 38,
            (2, 'MA101'): 91, (2, 'PH101'): 88, (2, 'CS101'): 85,
            (2, 'ME101'): 72, (2, 'EC101'): 80,
        }
        for (si, scode), marks in marks_map.items():
            if si < len(student_profiles) and scode in subjects:
                sub = subjects[scode]
                Result.objects.get_or_create(
                    student=student_profiles[si],
                    subject=sub,
                    semester=sub.semester,
                    academic_year='2024-25',
                    defaults={'marks_obtained': marks, 'entered_by': admin_user}
                )
        self.stdout.write(self.style.SUCCESS(f'  Created sample results'))

        self.stdout.write(self.style.SUCCESS('\n✅  Seed complete!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Admin   →  admin / admin123')
        self.stdout.write('  Student →  appaji / student123')
        self.stdout.write('  Student →  student2 / student123')
        self.stdout.write('  Student →  student3 / student123')
