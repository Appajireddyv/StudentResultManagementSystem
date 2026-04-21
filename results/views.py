from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from .models import StudentProfile, Subject, Result, Department
from .forms import (LoginForm, StudentForm, SubjectForm, ResultForm,
                    DepartmentForm, UserCreateForm)
from decimal import Decimal


def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser


# ── Authentication ────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'results/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ── Dashboard ─────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    if is_admin(request.user):
        return admin_dashboard(request)
    return student_dashboard(request)


def admin_dashboard(request):
    total_students = StudentProfile.objects.count()
    total_subjects = Subject.objects.count()
    total_results  = Result.objects.count()
    departments    = Department.objects.annotate(student_count=Count('studentprofile'))
    recent_results = Result.objects.select_related('student__user', 'subject').order_by('-entered_at')[:10]
    context = {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_results':  total_results,
        'departments':    departments,
        'recent_results': recent_results,
        'is_admin': True,
    }
    return render(request, 'results/admin_dashboard.html', context)


def student_dashboard(request):
    try:
        profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Student profile not found. Contact admin.')
        return redirect('login')
    results = Result.objects.filter(student=profile).select_related('subject')
    semesters = sorted(set(r.semester for r in results))
    context = {
        'profile':   profile,
        'results':   results,
        'semesters': semesters,
        'is_admin':  False,
    }
    return render(request, 'results/student_dashboard.html', context)


# ── Student Management ────────────────────────────────────────────────────────

@login_required
def student_list(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    q = request.GET.get('q', '')
    dept = request.GET.get('dept', '')
    students = StudentProfile.objects.select_related('user', 'department')
    if q:
        students = students.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(roll_number__icontains=q)
        )
    if dept:
        students = students.filter(department_id=dept)
    departments = Department.objects.all()
    context = {'students': students, 'departments': departments, 'q': q, 'dept': dept}
    return render(request, 'results/student_list.html', context)


@login_required
def student_add(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    user_form    = UserCreateForm(request.POST or None)
    profile_form = StudentForm(request.POST or None)
    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data['password'])
        user.save()
        student_group, _ = Group.objects.get_or_create(name='Student')
        user.groups.add(student_group)
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        messages.success(request, f'Student {user.get_full_name()} added successfully.')
        return redirect('student_list')
    return render(request, 'results/student_form.html', {
        'user_form': user_form, 'profile_form': profile_form, 'action': 'Add'
    })


@login_required
def student_edit(request, pk):
    if not is_admin(request.user):
        return redirect('dashboard')
    profile   = get_object_or_404(StudentProfile, pk=pk)
    user_form    = UserCreateForm(request.POST or None, instance=profile.user, edit_mode=True)
    profile_form = StudentForm(request.POST or None, instance=profile)
    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, 'Student updated successfully.')
        return redirect('student_list')
    return render(request, 'results/student_form.html', {
        'user_form': user_form, 'profile_form': profile_form, 'action': 'Edit', 'profile': profile
    })


@login_required
def student_delete(request, pk):
    if not is_admin(request.user):
        return redirect('dashboard')
    profile = get_object_or_404(StudentProfile, pk=pk)
    if request.method == 'POST':
        profile.user.delete()
        messages.success(request, 'Student deleted.')
        return redirect('student_list')
    return render(request, 'results/confirm_delete.html', {'object': profile, 'type': 'Student'})


@login_required
def student_detail(request, pk):
    if not is_admin(request.user):
        return redirect('dashboard')
    profile  = get_object_or_404(StudentProfile, pk=pk)
    results  = Result.objects.filter(student=profile).select_related('subject')
    semesters = sorted(set(r.semester for r in results))
    context  = {'profile': profile, 'results': results, 'semesters': semesters, 'is_admin': True}
    return render(request, 'results/student_detail.html', context)


# ── Subject Management ────────────────────────────────────────────────────────

@login_required
def subject_list(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    subjects = Subject.objects.select_related('department').order_by('semester', 'code')
    return render(request, 'results/subject_list.html', {'subjects': subjects})


@login_required
def subject_add(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    form = SubjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Subject added.')
        return redirect('subject_list')
    return render(request, 'results/subject_form.html', {'form': form, 'action': 'Add'})


@login_required
def subject_edit(request, pk):
    if not is_admin(request.user):
        return redirect('dashboard')
    subject = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(request.POST or None, instance=subject)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Subject updated.')
        return redirect('subject_list')
    return render(request, 'results/subject_form.html', {'form': form, 'action': 'Edit'})


@login_required
def subject_delete(request, pk):
    if not is_admin(request.user):
        return redirect('dashboard')
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted.')
        return redirect('subject_list')
    return render(request, 'results/confirm_delete.html', {'object': subject, 'type': 'Subject'})


# ── Marks / Results Management ───────────────────────────────────────────────

@login_required
def result_list(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    results  = Result.objects.select_related('student__user', 'subject').order_by('-entered_at')
    students = StudentProfile.objects.select_related('user')
    subjects = Subject.objects.all()
    student_id = request.GET.get('student')
    subject_id = request.GET.get('subject')
    semester   = request.GET.get('semester')
    if student_id:
        results = results.filter(student_id=student_id)
    if subject_id:
        results = results.filter(subject_id=subject_id)
    if semester:
        results = results.filter(semester=semester)
    context = {
        'results': results, 'students': students, 'subjects': subjects,
        'sel_student': student_id, 'sel_subject': subject_id, 'sel_semester': semester,
    }
    return render(request, 'results/result_list.html', context)


@login_required
def result_add(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    form = ResultForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        result = form.save(commit=False)
        result.entered_by = request.user
        result.save()
        messages.success(request, f'Marks entered for {result.student} – {result.subject.code}.')
        return redirect('result_list')
    return render(request, 'results/result_form.html', {'form': form, 'action': 'Add'})


@login_required
def result_edit(request, pk):
    if not is_admin(request.user):
        return redirect('dashboard')
    result = get_object_or_404(Result, pk=pk)
    form   = ResultForm(request.POST or None, instance=result)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Result updated.')
        return redirect('result_list')
    return render(request, 'results/result_form.html', {'form': form, 'action': 'Edit'})


@login_required
def result_delete(request, pk):
    if not is_admin(request.user):
        return redirect('dashboard')
    result = get_object_or_404(Result, pk=pk)
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Result deleted.')
        return redirect('result_list')
    return render(request, 'results/confirm_delete.html', {'object': result, 'type': 'Result'})


# ── Marksheet / Student Result View ──────────────────────────────────────────

@login_required
def my_marksheet(request):
    try:
        profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('dashboard')
    semester = request.GET.get('semester')
    results  = Result.objects.filter(student=profile).select_related('subject')
    if semester:
        results = results.filter(semester=semester)
    semesters = sorted(set(Result.objects.filter(student=profile).values_list('semester', flat=True)))
    # Compute GPA per semester
    sem_data = {}
    for r in Result.objects.filter(student=profile).select_related('subject'):
        s = r.semester
        if s not in sem_data:
            sem_data[s] = {'credits': 0, 'weighted': 0, 'results': []}
        sem_data[s]['results'].append(r)
        sem_data[s]['credits']  += r.subject.credits
        sem_data[s]['weighted'] += r.grade_point * r.subject.credits

    for s in sem_data:
        c = sem_data[s]['credits']
        sem_data[s]['gpa'] = round(sem_data[s]['weighted'] / c, 2) if c else 0

    context = {
        'profile':  profile,
        'results':  results,
        'semesters': semesters,
        'sem_data': sem_data,
        'sel_semester': semester,
    }
    return render(request, 'results/marksheet.html', context)


# ── API – Chart Data ──────────────────────────────────────────────────────────

@login_required
def chart_data(request):
    """Returns JSON chart data for the logged-in student."""
    try:
        profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return JsonResponse({'error': 'Not a student'}, status=403)

    semester = request.GET.get('semester')
    results  = Result.objects.filter(student=profile).select_related('subject')
    if semester:
        results = results.filter(semester=semester)

    labels     = [r.subject.code for r in results]
    marks      = [float(r.marks_obtained) for r in results]
    max_marks  = [r.subject.max_marks for r in results]
    colors     = ['#28a745' if r.is_pass else '#dc3545' for r in results]

    return JsonResponse({
        'labels':    labels,
        'marks':     marks,
        'max_marks': max_marks,
        'colors':    colors,
    })


# ── Department Management ────────────────────────────────────────────────────

@login_required
def department_list(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    departments = Department.objects.annotate(
        student_count=Count('studentprofile'),
        subject_count=Count('subject'),
    )
    return render(request, 'results/department_list.html', {'departments': departments})


@login_required
def department_add(request):
    if not is_admin(request.user):
        return redirect('dashboard')
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Department added.')
        return redirect('department_list')
    return render(request, 'results/department_form.html', {'form': form, 'action': 'Add'})


@login_required
def department_edit(request, pk):
    if not is_admin(request.user):
        return redirect('dashboard')
    dept = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=dept)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Department updated.')
        return redirect('department_list')
    return render(request, 'results/department_form.html', {'form': form, 'action': 'Edit'})
