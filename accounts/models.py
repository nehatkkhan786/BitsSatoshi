from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .utils import generate_code
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
	def create_user(self,email,first_name, username, last_name, password=None, *args, **kwargs):
		if not email:
			raise ValueError('User must have an email')

		user= self.model(
			email = self.normalize_email(email),
            first_name = first_name,
			last_name = last_name,
			username = username,
			)
		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self, first_name, last_name, email, username, password=None, **other_fields):
		user = self.create_user(
			email=self.normalize_email(email),
			username = username,
			password = password,
			first_name=first_name,
			last_name=last_name,
			)

		user.is_admin = True
		user.is_active = True
		user.is_staff = True
		user.is_superadmin = True
		user.save(using=self._db)
		return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	username = models.CharField(max_length=100, unique=True)
	email = models.EmailField(unique=True)

	#required Fields
	date_joined = models.DateTimeField(auto_now_add=True)
	last_login= models.DateTimeField(auto_now_add=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superadmin= models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
	objects = CustomUserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, add_label):
		return True


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_code()
            self.code =code
       	super().save(*args, **kwargs)
	