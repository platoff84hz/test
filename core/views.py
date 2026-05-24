from collections import Counter
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BootstrapAuthenticationForm, DirectionForm, TeacherForm, TeacherSelfForm
from .models import Direction, Teacher
from .models import Teacher, Direction, Subject
from .forms import TeacherForm, DirectionForm, SubjectForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


def auth_context(request):
    return {'login_form': BootstrapAuthenticationForm(request)}


def home(request):
    return render(request, 'core/home.html', auth_context(request) | {'title': 'Кафедра ИС УлГТУ'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = BootstrapAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Вход выполнен.')
            return redirect(request.POST.get('next') or 'home')
        messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'core/login.html', {
        'form': form,
        'login_form': form,
        'title': 'Вход',
        'hide_auth_panel': True,
    })


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Вы вышли из системы.')
    return redirect('home')


def teacher_list(request):
    teachers = Teacher.objects.prefetch_related('directions').select_related('user')
    query = request.GET.get('q', '').strip()
    position = request.GET.get('position', '').strip()

    if query:
        teachers = teachers.filter(
            Q(full_name__icontains=query)
            | Q(position__icontains=query)
            | Q(academic_title__icontains=query)
        )
    if position:
        teachers = teachers.filter(position=position)

    paginator = Paginator(teachers, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)

    context = auth_context(request) | {
        'title': 'Преподаватели',
        'page_obj': page_obj,
        'positions': Teacher.POSITION_CHOICES,
        'query': query,
        'position': position,
        'query_string': urlencode(params, doseq=True),
    }
    return render(request, 'core/teacher_list.html', context)


def can_edit_teacher(user, teacher):
    if is_admin(user):
        return True
    return user.is_authenticated and teacher.user_id == user.id


@user_passes_test(is_admin)
def teacher_create(request):
    form = TeacherForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Преподаватель добавлен.')
        return redirect('teachers')
    return render(request, 'core/form.html', auth_context(request) | {
        'title': 'Добавить преподавателя',
        'form': form,
        'submit_label': 'Сохранить',
    })


@login_required
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if not can_edit_teacher(request.user, teacher):
        return HttpResponseForbidden('Можно редактировать только свою карточку.')
    form_class = TeacherForm if is_admin(request.user) else TeacherSelfForm
    form = form_class(request.POST or None, instance=teacher)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Карточка преподавателя обновлена.')
        return redirect('teachers')
    return render(request, 'core/form.html', auth_context(request) | {
        'title': 'Редактировать преподавателя',
        'form': form,
        'submit_label': 'Сохранить',
    })


@user_passes_test(is_admin)
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Преподаватель удален.')
        return redirect('teachers')
    return render(request, 'core/confirm_delete.html', auth_context(request) | {
        'title': 'Удалить преподавателя',
        'object_name': teacher.full_name,
        'cancel_url': reverse('teachers'),
    })


def direction_list(request):
    directions = Direction.objects.all()
    paginator = Paginator(directions, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    counts = Counter(direction.qualification for direction in page_obj.object_list)
    seen = set()
    rows = []
    for direction in page_obj.object_list:
        first_in_group = direction.qualification not in seen
        seen.add(direction.qualification)
        rows.append({
            'direction': direction,
            'show_qualification': first_in_group,
            'rowspan': counts[direction.qualification],
        })

    return render(request, 'core/direction_list.html', auth_context(request) | {
        'title': 'Направления подготовки',
        'page_obj': page_obj,
        'rows': rows,
    })


@user_passes_test(is_admin)
def direction_create(request):
    form = DirectionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Направление добавлено.')
        return redirect('directions')
    return render(request, 'core/form.html', auth_context(request) | {
        'title': 'Добавить направление',
        'form': form,
        'submit_label': 'Сохранить',
    })


@user_passes_test(is_admin)
def direction_update(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    form = DirectionForm(request.POST or None, instance=direction)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Направление обновлено.')
        return redirect('directions')
    return render(request, 'core/form.html', auth_context(request) | {
        'title': 'Редактировать направление',
        'form': form,
        'submit_label': 'Сохранить',
    })


@user_passes_test(is_admin)
def direction_delete(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    if request.method == 'POST':
        direction.delete()
        messages.success(request, 'Направление удалено.')
        return redirect('directions')
    return render(request, 'core/confirm_delete.html', auth_context(request) | {
        'title': 'Удалить направление',
        'object_name': str(direction),
        'cancel_url': reverse('directions'),
    })


def subject_list(request):
    """Список дисциплин с фильтрацией по преподавателю"""
    subjects = Subject.objects.select_related('teacher').all()
    
    # Фильтр по преподавателю
    teacher_id = request.GET.get('teacher', '')
    if teacher_id:
        subjects = subjects.filter(teacher_id=teacher_id)
    
    # Поиск по названию
    query = request.GET.get('q', '').strip()
    if query:
        subjects = subjects.filter(name__icontains=query)
    
    # Пагинация
    paginator = Paginator(subjects, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    # Список преподавателей для фильтра
    teachers = Teacher.objects.all()
    
    context = auth_context(request) | {
        'title': 'Дисциплины',
        'page_obj': page_obj,
        'teachers': teachers,
        'selected_teacher': teacher_id,
        'query': query,
    }
    return render(request, 'core/subject_list.html', context)

@user_passes_test(is_admin)
def subject_create(request):
    """Создание новой дисциплины (только админ)"""
    form = SubjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Дисциплина добавлена.')
        return redirect('subjects')
    return render(request, 'core/form.html', auth_context(request) | {
        'title': 'Добавить дисциплину',
        'form': form,
        'submit_label': 'Сохранить',
    })

@user_passes_test(is_admin)
def subject_update(request, pk):
    """Редактирование дисциплины (только админ)"""
    subject = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(request.POST or None, instance=subject)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Дисциплина обновлена.')
        return redirect('subjects')
    return render(request, 'core/form.html', auth_context(request) | {
        'title': 'Редактировать дисциплину',
        'form': form,
        'submit_label': 'Сохранить',
    })

@user_passes_test(is_admin)
def subject_delete(request, pk):
    """Удаление дисциплины (только админ)"""
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Дисциплина удалена.')
        return redirect('subjects')
    return render(request, 'core/confirm_delete.html', auth_context(request) | {
        'title': 'Удалить дисциплину',
        'object_name': str(subject),
        'cancel_url': reverse('subjects'),
    })