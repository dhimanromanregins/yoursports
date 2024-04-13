from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_school = models.BooleanField(default=False)
    is_corporate = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'institution', 'address', 'is_school', 'is_corporate']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Pricing(models.Model):
    amount = models.BigIntegerField()
    description = models.TextField()
    gerneral = models.BooleanField(default=False)
    school_corporate = models.BooleanField(default=False)

    def __str__(self):
        return self.amount


class Contact(models.Model):
    fullname = models.CharField(max_length=255, null=True, blank=True)
    phone = models.BigIntegerField()
    email = models.EmailField()
    subject = models.CharField(max_length=1000)
    message = models.TextField()

    def __str__(self):
        return self.fullname


class PasswordResetToken(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.user



class FootballTeam(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    coach = models.CharField(max_length=100)
    captain = models.CharField(max_length=100)
    team_logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)

    def __str__(self):
        return self.name


class PlayerDetail(models.Model):
    football_team = models.ForeignKey(FootballTeam, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    no_goals = models.BigIntegerField()
    no_matches = models.BigIntegerField()

    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(max_length=2000)
    answer = models.TextField()



