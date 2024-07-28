from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobile=mobile)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile, password=None):
        user = self.create_user(email, name, mobile, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    def __str__(self):
        return self.email
    

from django.db import models
from django.conf import settings

class Expense(models.Model):
    SPLIT_METHOD_CHOICES = [
        ('equal', 'Equal'),
        ('exact', 'Exact'),
        ('percentage', 'Percentage'),
    ]

    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_method = models.CharField(max_length=10, choices=SPLIT_METHOD_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_expenses', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Participant(models.Model):
    expense = models.ForeignKey(Expense, related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='participated_expenses', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.expense.title}"