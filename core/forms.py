from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Direction, Teacher, Subject


class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
    )


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user', 'full_name', 'position', 'academic_title', 'photo_url', 'bio', 'directions']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'academic_title': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_url': forms.URLInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'directions': forms.CheckboxSelectMultiple(),
        }


class TeacherSelfForm(TeacherForm):
    class Meta(TeacherForm.Meta):
        fields = ['full_name', 'position', 'academic_title', 'photo_url', 'bio', 'directions']


class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = ['qualification', 'code', 'name', 'profile']
        widgets = {
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'hours', 'semester', 'teacher', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        