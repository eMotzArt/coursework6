from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'пользователь'),
        (ADMIN, 'администратор')
    ]

    phone = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default=USER)
    image = models.ImageField()

    class Meta:
        ordering = ['username']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.pk}: {self.username} ({self.first_name} {self.last_name})"
