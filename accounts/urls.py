from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgotPassword/', views.forgot_password, name='forgot_password'),
    path('resetpassword_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('resetPassword/', views.reset_password, name='reset_password'),
]
