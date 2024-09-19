from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from .mixins import ResizeImageMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from typing import List

def user_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return 'images/{0}/logo/{1}'.format(instance.id, "logo." + ext)


class UserManager(BaseUserManager):
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
            raise ValueError('Superuser must have is_staff=True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)

# базовий клас користувача
class User(AbstractUser, ResizeImageMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    username = models.UUIDField(default=uuid.uuid4)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    first_name = models.CharField(verbose_name="Ім'я", max_length=64, blank=True)
    middle_name = models.CharField(verbose_name="По батькові", max_length=64, blank=True)
    last_name = models.CharField(verbose_name="Призвище", max_length=64, blank=True)
    email = models.EmailField(unique=True)

    photo = models.ImageField('Зображення', upload_to=user_path, null=True, blank=True)
    phone = models.CharField(verbose_name="Телефон", max_length=16, blank=True)


    is_confirmed = models.BooleanField("Підтверджено", default=False)
    creation_rules = models.BooleanField("Право створення", default=True)
    comment_rules = models.BooleanField("Право коментування", default=False)
    profile_view_rules = models.BooleanField("Право перегляду профілей", default=False)

    show_email = models.BooleanField("Показувати ел.пошту", default=False)
    show_phone = models.BooleanField("Показувати телефон", default=False)

    objects = UserManager()

    def save(self, *args, **kwargs):
        # print(kwargs, args)

        field: List  = kwargs.get("update_fields")

        if not field and self.photo:
            self.resize(self.photo, (500, 500))
            
        super(User, self).save(*args, **kwargs)

# нові поля для опису користувача
class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)  
    birth_date = models.DateField("Дата народження", null=True, blank=True) 
    show_birth_date = models.BooleanField("Показувати дату народження", null=True, blank=True)
    status = models.CharField("Статус",max_length=100, blank=True) 
    description = models.TextField("Інформація", blank=True) 

    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = 'Користувачі > Профіль'
        verbose_name_plural = 'Профілі користувачів'
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
