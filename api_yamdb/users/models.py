from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLE_NAME = 'user'
    MODERATOR_ROLE_NAME = 'moderator'
    ADMIN_ROLE_NAME = 'admin'

    AVAILABLE_USER_ROLES = (
        (USER_ROLE_NAME, 'User'),
        (MODERATOR_ROLE_NAME, 'Moderator'),
        (ADMIN_ROLE_NAME, 'Admin')
    )

    email = models.EmailField(
        'Email address',
        unique=True,
        blank=False,
        null=False
    )
    bio = models.TextField(
        'Biography',
        blank=True
    )
    role = models.CharField(
        'Role',
        max_length=20,
        default=USER_ROLE_NAME,
        choices=AVAILABLE_USER_ROLES,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN_ROLE_NAME

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR_ROLE_NAME

    @property
    def is_user(self):
        return self.role == self.USER_ROLE_NAME
