from django.db import models

class Course(models.Model):
    nama = models.CharField(max_length=200)

    def __str__(self):
        return self.nama

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    judul = models.CharField(max_length=200)

    def __str__(self):
        return self.judul

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    teks = models.TextField()

    def __str__(self):
        return self.teks

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    teks = models.CharField(max_length=200)
    benar = models.BooleanField(default=False)

    def __str__(self):
        return self.teks
        
