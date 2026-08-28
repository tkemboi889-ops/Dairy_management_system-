from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from .forms import registration_form
# implementing registration of  new user
class SignUpView(CreateView):
    form_class = registration_form
    template_name = "registration/sign_up.html"
    success_url = "/login/"
#implementing login and logout django authentication
class UserLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True
# implementing logout
class UserLogoutView(LogoutView):
    template_name = "registration/logout.html"