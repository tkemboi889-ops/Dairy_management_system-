from django.contrib.auth.forms import UserCreationForm
from .models import Management
class registration_form(UserCreationForm):
    class Meta:
        model=Management
        fields="__all__"
        