from django.urls import path

from accounts.views import login_view, logout_view, register_view, UserDetailView, UserChangeView, \
    UserChangePasswordView, UserListView
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('profile/<pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/<pk>/edit/', UserChangeView.as_view(), name='user_update'),
    path('profile/<pk>/change-password/', UserChangePasswordView.as_view(), name='user_change_password'),
    path('profiles/', UserListView.as_view(), name='users')

]

app_name = 'accounts'
