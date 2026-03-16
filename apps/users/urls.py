from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/settings/', views.dashboard_settings, name='dashboard_settings'),
]
