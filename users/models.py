from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from users.manager import UserManager


class User(AbstractUser):
    objects = UserManager()

    #roles
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'пользователь'),
        (ADMIN, 'администратор'),
    ]

    #fields
    phone = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default=USER)
    image = models.ImageField()
    username = models.CharField(null=True, blank=True, max_length=150)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]
    #
    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        ordering = ['username']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.pk}: {self.username} ({self.first_name} {self.last_name})"