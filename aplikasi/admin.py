from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Course, Lesson, Pertanyaan, Pilihan, Submission


class PilihanInline(admin.TabularInline):
    model = Pilihan
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Pertanyaan
    extra = 1


class ChoiceInline(PilihanInline):
    pass


class QuestionAdmin(admin.ModelAdmin):
    inlines = [PilihanInline]
    list_display = ("teks", "lesson")
    search_fields = ["teks"]


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ("judul", "course")
    list_filter = ["course"]


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("pengguna", "pertanyaan", "benar", "tanggal")
    list_filter = ["benar", "tanggal"]


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff")


@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Pertanyaan, QuestionAdmin)
admin.site.register(Submission, SubmissionAdmin)
