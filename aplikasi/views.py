from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Course, Lesson, Question, Choice, Submission


def daftar_kursus(request):
    kursus = Course.objects.all()
    return render(request, 'daftar_kursus.html', {'kursus': kursus})


def detail_kursus(request, pk):
    kursus = get_object_or_404(Course, pk=pk)
    pelajaran = kursus.lesson_set.all()
    return render(request, 'course_details_bootstrap.html', {'course': kursus, 'lessons': pelajaran})


def ujian(request, lesson_id):
    pelajaran = get_object_or_404(Lesson, pk=lesson_id)
    pertanyaan = pelajaran.question_set.all()
    return render(request, 'ujian.html', {'lesson': pelajaran, 'questions': pertanyaan})


def submit(request, lesson_id):
    pelajaran = get_object_or_404(Lesson, pk=lesson_id)
    
    for pertanyaan in pelajaran.question_set.all():
        pilihan_terpilih = request.POST.get(f'pertanyaan_{pertanyaan.id}')
        
        if pilihan_terpilih:
            pilihan = get_object_or_404(Choice, pk=pilihan_terpilih)
            
            kirim = Submission.objects.create(
                siswa=request.user,
                pertanyaan=pertanyaan
            )
            kirim.pilihan_dipilih.add(pilihan)
    
    return redirect('show_exam_result', lesson_id=lesson_id)


def show_exam_result(request, lesson_id):
    pelajaran = get_object_or_404(Lesson, pk=lesson_id)
    total_soal = pelajaran.question_set.count()
    benar = 0
    
    for pertanyaan in pelajaran.question_set.all():
        kirim = Submission.objects.filter(
            siswa=request.user,
            pertanyaan=pertanyaan
        ).first()
        
        if kirim:
            pilihan = kirim.pilihan_dipilih.first()
            if pilihan and pilihan.benar:
                benar += 1
    
    skor = int((benar / total_soal) * 100) if total_soal > 0 else 0
    
    return render(request, 'hasil_ujian.html', {
        'lesson': pelajaran,
        'skor': skor,
        'benar': benar,
        'total': total_soal
    })
