from django.contrib import admin
from .models import Course, Lesson, Student

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    filter_horizontal = ('enrolled_courses', 'completed_lessons')
