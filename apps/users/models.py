from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, full_name='', active=False):
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(
            email=UserManager.normalize_email(email),
            full_name=full_name,
        )
        if password:
            user.set_password(password)
        user.is_active = active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, full_name=''):
        """
        Creates and saves a superuser with the given email, full name and password.
        """
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            active=True,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email address', max_length=255, unique=True, db_index=True)
    full_name = models.CharField(max_length=245)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, app_label):
        return self.is_staff
