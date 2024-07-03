from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, NewPasswordView, UserUpdateView, UserProfileView, \
    UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('new-password/', NewPasswordView.as_view(), name='new_password'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile-edit/', UserUpdateView.as_view(), name='profile_edit'),
    path('profile-delete/<int:pk>/', UserDeleteView.as_view(), name='profile_delete'),
]