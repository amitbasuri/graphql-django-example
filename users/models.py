from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser):
    username = None
    SKILLS = (
        ('DEV', 'Developer'),
        ('QA', 'Quality Analyst'),
        ('BDE', 'Business Development Executive'),
        ('BA', 'Business Analyst'),
        ('HR', 'Human Resource Executive')
    )

    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    email = models.EmailField('email address', unique=True)
    password = models.CharField(max_length=500)
    profile_image_url = models.URLField()
    gender = models.CharField(max_length=1, choices=GENDERS)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=30)
    skill = models.CharField(max_length=20, choices=SKILLS)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'password', 'gender']

    objects = UserManager()

    def get_by_natural_key(self, username):
        return self.get(**{'{}__iexact'.format(self.model.USERNAME_FIELD): username})

    def __str__(self):
        return self.email
