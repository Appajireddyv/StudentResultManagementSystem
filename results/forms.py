from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, Subject, Result, Department


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.edit_mode = kwargs.pop('edit_mode', False)
        super().__init__(*args, **kwargs)
        if self.edit_mode:
            self.fields['password'].help_text = 'Leave blank to keep existing password.'

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd  = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model  = StudentProfile
        fields = ['roll_number', 'department', 'current_semester', 'phone', 'date_of_birth']
        widgets = {
            'roll_number':       forms.TextInput(attrs={'class': 'form-control'}),
            'department':        forms.Select(attrs={'class': 'form-select'}),
            'current_semester':  forms.NumberInput(attrs={'class': 'form-control'}),
            'phone':             forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth':     forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model  = Subject
        fields = ['name', 'code', 'department', 'semester', 'max_marks', 'credits']
        widgets = {
            'name':       forms.TextInput(attrs={'class': 'form-control'}),
            'code':       forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'semester':   forms.NumberInput(attrs={'class': 'form-control'}),
            'max_marks':  forms.NumberInput(attrs={'class': 'form-control'}),
            'credits':    forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ResultForm(forms.ModelForm):
    class Meta:
        model  = Result
        fields = ['student', 'subject', 'marks_obtained', 'semester', 'academic_year']
        widgets = {
            'student':        forms.Select(attrs={'class': 'form-select'}),
            'subject':        forms.Select(attrs={'class': 'form-select'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'semester':       forms.NumberInput(attrs={'class': 'form-control'}),
            'academic_year':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2024-25'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model  = Department
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }
