from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2

class CourseAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('judul', 'course')
    list_filter = ('course',)
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('teks', 'lesson')
    list_filter = ('lesson',)
    inlines = [ChoiceInline]

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('teks', 'question', 'benar')
    list_filter = ('benar', 'question')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'pertanyaan', 'tanggal_kirim')
    list_filter = ('tanggal_kirim', 'siswa')
    readonly_fields = ('tanggal_kirim',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Submission, SubmissionAdmin)
