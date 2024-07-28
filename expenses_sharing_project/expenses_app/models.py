from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)  # Normalize the email address
        user = self.model(email=email, name=name, mobile=mobile)  # Create a new user instance
        user.set_password(password)  # Set the user's password
        user.save(using=self._db)  # Save the user to the database
        return user

    def create_superuser(self, email, name, mobile, password=None):
        user = self.create_user(email, name, mobile, password)  # Create a regular user
        user.is_admin = True  # Set the user as an admin
        user.save(using=self._db)  # Save the user to the database
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)  # User's email address
    name = models.CharField(max_length=255)  # User's name
    mobile = models.CharField(max_length=15)  # User's mobile number
    is_active = models.BooleanField(default=True)  # Indicates if the user account is active
    is_admin = models.BooleanField(default=False)  # Indicates if the user is an admin

    objects = UserManager()  # Associate UserManager with User

    USERNAME_FIELD = 'email'  # Field used for authentication
    REQUIRED_FIELDS = ['name', 'mobile']  # Required fields for creating a user

    def __str__(self):
        return self.email  # String representation of the user
    

from django.db import models
from django.conf import settings

class Expense(models.Model):
    SPLIT_METHOD_CHOICES = [
        ('equal', 'Equal'),
        ('exact', 'Exact'),
        ('percentage', 'Percentage'),
    ]

    title = models.CharField(max_length=255)  # Title of the expense
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total amount of the expense
    split_method = models.CharField(max_length=10, choices=SPLIT_METHOD_CHOICES)  # Method to split the expense
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_expenses', on_delete=models.CASCADE)  # User who created the expense
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the expense was created

    def __str__(self):
        return self.title  # String representation of the expense
    

class Participant(models.Model):
    expense = models.ForeignKey(Expense, related_name='participants', on_delete=models.CASCADE)  # Related expense
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='participated_expenses', on_delete=models.CASCADE)  # User participating in the expense
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Amount owed by the participant
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Percentage owed by the participant

    def __str__(self):
        return f"{self.user.email} - {self.expense.title}"  # String representation of the participant