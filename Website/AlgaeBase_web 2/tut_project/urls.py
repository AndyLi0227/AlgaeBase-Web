from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static
from Cramatch import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Cramatch.urls')), #'name#'
    #########################################################
    path('register/', user_views.register, name='register'),
    path('student_register/', user_views.student_register.as_view(), name='student_register'),
    path('tutor_register/', user_views.tutor_register.as_view(), name='tutor_register'),
    path('school_register/', user_views.school_register.as_view(), name='school_register'),
    #########################################################

    ######################tutor url ###############################
    path('JobPool/', user_views.JobPool, name='JobPool'),
    path('Job/<int:pk>/', user_views.Job, name='Job'),
    path('Job/<int:pk>/apply', views.applyJob, name='applyJob'),
    path('Job/<int:pk>/approve', views.applyJobApprove, name='applyJobApprove'),
    path('Job/<int:pk>/open', views.applyJobOpen, name='applyJobOpen'),
    path('Job/<int:pk>/close', views.applyJobClose, name='applyJobClose'),
    ###################################################################

    ######################student url ###############################
    #path('exam/', user_views.exam, name='exam'),
    ###################################################################

    ######################price and class information url ###############################
    path('infoClass/', user_views.infoClass, name='infoClass'),
    ###################################################################
    
    # path('testpage/',views.testpage, name='testpage'),
    ######################school url ###############################
    path('Iclass/', user_views.ClassListView, name='Iclass'),
    path('Iclass/<int:pk>/', user_views.ClassDetailView, name='Iclass-detail'),
    path('Iclass/new/', user_views.ClassCreateView, name='Iclass-create'),
    path('Iclass/<int:pk>/update', user_views.ClassUpdateView, name='Iclass-update'),
    path('Iclass/<int:pk>/delete', user_views.ClassDelete, name='Iclass-delete'),
    ###################################################################
    path('profile/', user_views.profile, name='profile'),
    path('schedule/', user_views.schedule, name='schedule'),
    path('login/',LoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('logout/',LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    path('password-reset/',PasswordResetView.as_view(template_name = 'users/password_reset.html'), name='password_reset'),
    path('password-reset/done/',PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)