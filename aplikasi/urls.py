from django.urls import path
from . import views

urlpatterns = [
    path("", views.daftar_kursus, name="daftar_kursus"),
    path("ujian/<int:lesson_id>/", views.mulai_ujian, name="mulai_ujian"),
    path("ujian/submit/", views.submit, name="submit"),
    path(
        "hasil/<int:skor>/<int:total>/<int:persen>/<int:lesson_id>/",
        views.show_exam_result,
        name="show_exam_result"
    ),
]
