from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_kursus, name='daftar_kursus'),
    path('<int:pk>/', views.detail_kursus, name='detail_kursus'),
    path('<int:lesson_id>/ujian/', views.ujian, name='ujian'),
    path('<int:lesson_id>/submit/', views.submit, name='submit'),
    path('<int:lesson_id>/result/', views.show_exam_result, name='show_exam_result'),
]
