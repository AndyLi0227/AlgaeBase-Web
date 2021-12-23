from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('bypass',views.bypass, name='bypass'),
    path('', views.index, name='cramatch-index'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('stud_dash/', views.stud_dash, name='stud_dash'),
    path('school_dash/', views.school_dash, name='school_dash'),
    path('login_index/',views.loginIndex, name='login_index'),
    path('subscription/',views., name='subscription'),
] 

