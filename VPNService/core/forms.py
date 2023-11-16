from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from core.models import Guest


class NewGuestForm(UserCreationForm):
    class Meta:
        model = Guest
        fields = ["username", "email", "password1", "password2"]
