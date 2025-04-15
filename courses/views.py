from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Course, Lesson, Student
from .forms import CourseEnrollmentForm, CourseForm, LessonForm, UserUpdateForm
from .serializers import CourseSerializer


# ========== Student Enrollment ==========
def enroll_student(request):
    student = None

    if request.method == "POST":
        form = CourseEnrollmentForm(request.POST)
        if form.is_valid():
            student_name = form.cleaned_data["student_name"]
            student_email = form.cleaned_data["student_email"]
            course = form.cleaned_data["course"]

            student, created = Student.objects.get_or_create(email=student_email)
            if created or not student.name:
                student.name = student_name
                student.save()

            if course in student.enrolled_courses.all():
                messages.error(request, "You are already registered in this course.")
            else:
                student.enrolled_courses.add(course)
                return render(request, "courses/enrollment_success.html", {
                    "student_name": student_name,
                    "course": course,
                })
    else:
        form = CourseEnrollmentForm()

    return render(request, "courses/enroll_student.html", {"form": form, "student": student})


# ========== Course Views ==========

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        lessons = course.lessons.all()
        student = None
        completed_lesson_ids = []

        user = self.request.user
        if user.is_authenticated:
            try:
                student = Student.objects.get(email=user.email)
                completed_lesson_ids = student.completed_lessons.filter(course=course).values_list('id', flat=True)
            except Student.DoesNotExist:
                student = None

        context.update({
            'lessons': lessons,
            'student': student,
            'completed_lesson_ids': list(completed_lesson_ids),
            'progress_percent': int((len(completed_lesson_ids) / lessons.count()) * 100) if lessons.exists() else 0
        })
        return context


class CourseCreateView(CreateView):
    model = Course
    fields = ['title', 'description', 'duration', 'thumbnail']
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "✅ Course created successfully!")
        return response


def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect("course_list")
    else:
        form = CourseForm(instance=course)

    return render(request, "courses/course_form.html", {"form": form})


def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect("course_list")

    return render(request, "courses/course_confirm_delete.html", {"course": course})


def course_students_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.students.all()
    return render(request, 'courses/course_student_list.html', {'course': course, 'students': students})


# ========== Lesson Views ==========

def lesson_create(request):
    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson created successfully!")
            return redirect("course_list")
    else:
        form = LessonForm()
    return render(request, "courses/lesson_form.html", {"form": form})


def lesson_update(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson updated successfully!")
            return redirect("course_list")
    else:
        form = LessonForm(instance=lesson)

    return render(request, "courses/lesson_form.html", {"form": form})


def lesson_form_view(request, course_id, lesson_id=None):
    if lesson_id:
        lesson = get_object_or_404(Lesson, id=lesson_id)
        is_edit = True
    else:
        lesson = Lesson(course_id=course_id)
        is_edit = False

    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = LessonForm(instance=lesson)

    return render(request, "courses/lesson_form.html", {"form": form, "is_edit": is_edit})


def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        lesson.delete()
        messages.success(request, "Lesson deleted successfully!")
        return redirect("course_list")

    return render(request, "courses/lesson_confirm_delete.html", {"lesson": lesson})


# ========== Authentication ==========

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'courses/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Login successful!")
            return redirect('/')
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'courses/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('/')


@login_required(login_url='login')
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


def home(request):
    courses = Course.objects.all()
    form = CourseForm()
    return render(request, "courses/home.html", {"courses": courses, "form": form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'courses/profile.html', {'form': form})


# ========== API Views ==========

class CourseListAPI(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseDetailAPI(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course)
        return Response(serializer.data)


class EnrollStudentAPI(APIView):
    def post(self, request):
        student_email = request.data.get('email')
        student_name = request.data.get('name')
        course_id = request.data.get('course_id')

        if not all([student_email, student_name, course_id]):
            return Response({'error': 'Email, name, and course_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        student, _ = Student.objects.get_or_create(email=student_email)
        student.name = student_name
        student.save()
        student.enrolled_courses.add(course)

        return Response({'message': f'{student.name} has been enrolled in {course.title}'})
