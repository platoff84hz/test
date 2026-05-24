from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('teachers/', views.teacher_list, name='teachers'),
    path('teachers/add/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:pk>/edit/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),
    path('directions/', views.direction_list, name='directions'),
    path('directions/add/', views.direction_create, name='direction_create'),
    path('directions/<int:pk>/edit/', views.direction_update, name='direction_update'),
    path('directions/<int:pk>/delete/', views.direction_delete, name='direction_delete'),
    path('subjects/', views.subject_list, name='subjects'),
    path('subjects/add/', views.subject_create, name='subject_create'),
    path('subjects/<int:pk>/edit/', views.subject_update, name='subject_update'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),
]
