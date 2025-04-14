from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from courses.views import home,enroll_student,register,user_login,user_logout,profile,CourseListAPI,CourseDetailAPI,EnrollStudentAPI  # Import the enroll_student view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('enroll/', enroll_student, name='enroll_student'),  # Add this path for enroll
    
    # Lab-06
     path('', home, name='home'),  # Set homepage as the root path
     path("register/", register, name="register"),  # Add this line
    path("login/", user_login, name="login"),  # Add this line
     path("logout/", user_logout, name="logout"),  # Add this line
     path("profile/", profile, name = "profile"),
     path('password_change/', auth_views.PasswordChangeView.as_view(template_name='courses/password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='courses/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='courses/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='courses/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='courses/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='courses/password_reset_complete.html'), name='password_reset_complete'),
    
    
    path('api/courses/', CourseListAPI.as_view(), name='api_course_list'),
    path('api/courses/<int:pk>/', CourseDetailAPI.as_view(), name='api_course_detail'),
    
    path('api/enroll/', EnrollStudentAPI.as_view(), name='api_enroll_student'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
