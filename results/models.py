from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    current_semester = models.IntegerField(default=1)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"

    def get_full_name(self):
        return self.user.get_full_name()


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField()
    max_marks = models.IntegerField(default=100)
    credits = models.IntegerField(default=4)

    def __str__(self):
        return f"{self.code} - {self.name} (Sem {self.semester})"


class Result(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    semester = models.IntegerField()
    academic_year = models.CharField(max_length=20, default='2024-25')
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='entered_results')
    entered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'subject', 'semester', 'academic_year')

    @property
    def percentage(self):
        return (self.marks_obtained / self.subject.max_marks) * 100

    @property
    def grade(self):
        p = float(self.percentage)
        if p >= 90:
            return 'O'
        elif p >= 80:
            return 'A+'
        elif p >= 70:
            return 'A'
        elif p >= 60:
            return 'B+'
        elif p >= 50:
            return 'B'
        elif p >= 40:
            return 'C'
        else:
            return 'F'

    @property
    def grade_point(self):
        grade_map = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'F': 0}
        return grade_map.get(self.grade, 0)

    @property
    def is_pass(self):
        return float(self.percentage) >= 40

    def __str__(self):
        return f"{self.student} - {self.subject.code} - {self.grade}"
