from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Pertanyaan, Pilihan, Submission


def daftar_kursus(request):
    daftar = Course.objects.all()
    return render(request, "course_details_bootstrap.html", {"daftar_kursus": daftar})


@login_required
def mulai_ujian(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    pertanyaan_list = lesson.daftar_pertanyaan.all()
    return render(request, "ujian.html", {"lesson": lesson, "pertanyaan_list": pertanyaan_list})


@login_required
def submit(request):
    if request.method != "POST":
        return redirect("/")

    skor = 0
    total = 0
    lesson_id = None

    for key, value in request.POST.items():
        if key.startswith("pertanyaan_"):
            qid = int(key.split("_")[1])
            choice_id = int(value)
            pertanyaan = get_object_or_404(Pertanyaan, id=qid)
            pilihan = get_object_or_404(Pilihan, id=choice_id)

            if not lesson_id:
                lesson_id = pertanyaan.lesson.id

            benar = pilihan.benar
            Submission.objects.create(
                pengguna=request.user,
                pertanyaan=pertanyaan,
                pilihan_dipilih=pilihan,
                benar=benar
            )
            total += 1
            if benar:
                skor += 1

    persen = int((skor / total) * 100) if total > 0 else 0
    return redirect("show_exam_result", skor=skor, total=total, persen=persen, lesson_id=lesson_id)


def show_exam_result(request, skor, total, persen, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    berhasil = persen >= 70
    pesan = "Selamat! Anda berhasil lulus ujian." if berhasil else "Terima kasih telah mencoba, silakan ulangi lagi."

    return render(request, "hasil_ujian.html", {
        "lesson": lesson,
        "skor": skor,
        "total": total,
        "persen": persen,
        "berhasil": berhasil,
        "pesan": pesan
    })
