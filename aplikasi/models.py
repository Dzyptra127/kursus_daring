from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    nama = models.CharField(max_length=200)

    def __str__(self):
        return self.nama


class Lesson(models.Model):
    judul = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    def __str__(self):
        return self.judul


class Pertanyaan(models.Model):
    teks = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="daftar_pertanyaan")

    def __str__(self):
        return self.teks[:60]


class Pilihan(models.Model):
    pertanyaan = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE, related_name="pilihan")
    teks = models.CharField(max_length=255)
    benar = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.teks} {'(BENAR)' if self.benar else ''}"


class Submission(models.Model):
    pengguna = models.ForeignKey(User, on_delete=models.CASCADE)
    pertanyaan = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE)
    pilihan_dipilih = models.ForeignKey(Pilihan, on_delete=models.CASCADE, null=True, blank=True)
    benar = models.BooleanField(default=False)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pengguna.username} — {self.pertanyaan.teks[:30]}"
