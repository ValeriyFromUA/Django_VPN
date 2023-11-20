from core.models import Guest
from django.contrib.auth.forms import UserCreationForm


class NewGuestForm(UserCreationForm):
    class Meta:
        model = Guest
        fields = ["username", "email", "password1", "password2"]
