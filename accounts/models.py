import sys

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from random import choice
from string import ascii_lowercase, digits


class MyAccountManager(BaseUserManager):
    def create_user(self, name, email,username, phone_num=None, password=None):
        if not email:
            raise ValidationError('User must have an email address')
        if not name:
            raise ValidationError('User must have a name')

        username = generate_random_username(username=username)
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            username=username,
            # phone_num=phone_num
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            name=name,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_super_admin = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=254, unique=True)
    phone_num = models.CharField(max_length=15)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


def generate_random_username(username, length=0, chars=ascii_lowercase + digits, split=4, delimiter='-'):
    generated_username = username + ''.join([choice(chars) for _ in range(length)])
    # if split:
    #     username = delimiter.join([username[start:start + split] for start in range(0, len(username), split)])
    if Account.objects.filter(username=generated_username).exists():
        return generate_random_username(username=username, length=length+1, chars=chars)
    return generated_username

