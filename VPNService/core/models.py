from django.contrib.auth.models import AbstractUser
from django.db import models


class Guest(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=200, null=True, unique=True)
    is_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Відвідувач"
        verbose_name_plural = "Відвідувачі"


class Portals(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="guest_portal", null=False)
    domain = models.CharField(max_length=1000, null=False)
    portal_name = models.CharField(max_length=1000, null=False)
    data_volume = models.DecimalField(max_digits=10, decimal_places=2, help_text="Data volume in megabytes", default=0)
    page_views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Портал"
        verbose_name_plural = "Портали"
