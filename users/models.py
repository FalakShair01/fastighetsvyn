from django.db import models

# Create your models here.

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.text import slugify


def image_upload(instance, filename):
    return "/".join(["images", str(instance.name), filename])


def upload_to(instance, filename):
    return "/".join(["images", str(instance.username), filename])


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, phone, role, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email).lower(),
            username=username,
            phone=phone,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email, password=password, username=username, role="ADMIN", **kwargs
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    profile = models.ImageField(upload_to=upload_to, null=True, blank=True)
    ROLES = (("ADMIN", "Admin"), ("USER", "User"))
    role = models.CharField(max_length=10, choices=ROLES, default="USER")

    SUB_TYPE = (("TRIAL", "Trial"), ("ORIGNAL", "Orignal"))
    subscription_type = models.CharField(
        max_length=10, choices=SUB_TYPE, default="TRIAL"
    )
    SUB_STATUS = (("ACTIVE", "Active"), ("EXPIRED", "Expired"))
    subscription_status = models.CharField(
        max_length=7, choices=SUB_STATUS, default="ACTIVE"
    )
    allow_access_account = models.BooleanField(default=False)
    username_slug = models.SlugField(blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone", "address"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        if not self.username_slug:
            self.username_slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)


# imported here to avoid circular import
from property.models import Property


class Tenant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tenants")
    name = models.CharField(max_length=255)
    property = models.ForeignKey(
        Property, on_delete=models.SET_NULL, null=True
    )  # Add this line
    appartment_no = models.CharField(max_length=255)
    email = models.EmailField(verbose_name="Email", null=True, blank=False)
    phone = models.CharField(max_length=255)
    profile = models.ImageField(upload_to=image_upload, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    # class Meta:
    #     unique_together = ('user', 'email')

    def __str__(self):
        return self.name


class Managers(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="managers")
    email = models.EmailField()
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=150)
    password = models.CharField(max_length=25, null=True)
    role = models.CharField(max_length=7, default="Manager")
    is_active = models.BooleanField(default=True)


class ServiceProvider(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150, null=True)
    company = models.TextField(null=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class DemoRequests(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


# class ContactUs(models.Model):
# name = models.CharField(max_length=255)
# phone = models.CharField(max_length=255)
# email = models.EmailField()
# message = models.TextField()
# created_at = models.DateTimeField(auto_now_add=True)
# updated_at = models.DateTimeField(auto_now=True)
