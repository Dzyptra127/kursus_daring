from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission


def index(request):
    courses = Course.objects.all()
    return render(request, 'onlinecourse/course_list.html', {'courses': courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_detail.html', {'course': course})


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment, created = Enrollment.objects.get_or_create(learner=request.user.learner, course=course)
    
    selected_ids = []
    for key in request.POST:
        if key == 'choice':
            selected_ids.extend(request.POST.getlist(key))
    
    submission = Submission.objects.create(enrollment=enrollment)
    submission.choices.set(Choice.objects.filter(id__in=selected_ids))
    
    return HttpResponseRedirect(reverse('show_exam_result', args=(course_id, submission.id)))


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    total_score = 0
    earned_score = 0
    
    for question in course.question_set.all():
        selected_ids = list(submission.choices.filter(question=question).values_list('id', flat=True))
        if question.is_get_score(selected_ids):
            earned_score += question.grade
        total_score += question.grade
    
    score_percent = int((earned_score / total_score) * 100) if total_score > 0 else 0
    
    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'submission': submission,
        'grade': score_percent
    })
