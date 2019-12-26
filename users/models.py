from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import UserManager


class Country(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    phone_code = models.CharField(max_length=10, null=True)


class State(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)


class City(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_id = models.ForeignKey(State, on_delete=models.CASCADE)


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
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
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
