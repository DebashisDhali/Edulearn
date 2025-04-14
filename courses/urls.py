from django.urls import path
from .views import (
    register, user_login, user_logout, home,
    CourseListView, CourseDetailView, CourseCreateView,
     course_update, course_delete,
    lesson_create, lesson_update, lesson_delete,
    enroll_student, course_students_list,
)

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    
    path('<int:course_id>/update/', course_update, name='course_update'),
    path('<int:course_id>/delete/', course_delete, name='course_delete'),
    path('<int:course_id>/students/', course_students_list, name='course_students_list'),

    # Lesson URLs
    path('lesson/create/', lesson_create, name='lesson_create'),
    path('lesson/<int:lesson_id>/update/', lesson_update, name='lesson_update'),
    path('lesson/<int:lesson_id>/delete/', lesson_delete, name='lesson_delete'),

    # Enrollment
    path('enroll/', enroll_student, name='enroll_student'),

    # Auth
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # Home page
    path('home/', home, name='home'),
    
       
]
