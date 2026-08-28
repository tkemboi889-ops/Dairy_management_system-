from django.urls import path
from .Api_views import RegisterAPIView, LoginAPIView,LogoutView
from .views import UserLogoutView,UserLoginView,SignUpView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/',LogoutView.as_view(),name="logout"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/",UserLogoutView.as_view(),name="logout"),
    path("register/",SignUpView.as_view(),name="register"),
   path("password_change/",auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form.html"),name="password_change"),
   path("password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"),name="password_change_done"),
   path("password_reset/",auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),name="password_reset"),
   path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name="password_reset_done"),
   path("reset/<uid64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),name="password_reset_confirm"),
   path("rest/done/",auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),name="password_reset_complete"),
]
