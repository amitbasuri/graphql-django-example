from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        now = timezone.now()
        user = self.model(
            email=self.normalize_email(email),
            last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(**{'{}__iexact'.format(self.model.USERNAME_FIELD): username})

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)
