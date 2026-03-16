from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    """Manager for the custom User model using email as primary key."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model.
    Email is the primary key and cannot be changed after registration.
    """
    email = models.EmailField(
        primary_key=True,
        unique=True,
        verbose_name='Email',
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Nombre de usuario',
    )
    display_name = models.CharField(
        max_length=60,
        blank=True,
        verbose_name='Nombre visible',
    )
    bio = models.TextField(
        max_length=300,
        blank=True,
        verbose_name='Biografía',
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Foto de perfil',
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Ciudad / País',
    )
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.display_name or self.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def posts_count(self):
        return self.posts.count()


class Follow(models.Model):
    """Represents a follow relationship between two users."""
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Seguidor',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Seguido',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'Seguimiento'
        verbose_name_plural = 'Seguimientos'

    def __str__(self):
        return f'{self.follower.username} → {self.following.username}'
