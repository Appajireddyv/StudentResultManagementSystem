from django.contrib import admin
from .models import Department, StudentProfile, Subject, Result


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'get_full_name', 'department', 'current_semester']
    list_filter = ['department', 'current_semester']
    search_fields = ['roll_number', 'user__first_name', 'user__last_name']

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'semester', 'max_marks', 'credits']
    list_filter = ['department', 'semester']
    search_fields = ['code', 'name']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'marks_obtained', 'semester', 'academic_year', 'grade']
    list_filter = ['semester', 'academic_year', 'subject__department']
    search_fields = ['student__roll_number', 'student__user__first_name']

    def grade(self, obj):
        return obj.grade
    grade.short_description = 'Grade'
