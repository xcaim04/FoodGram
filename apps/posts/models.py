from django.db import models
from django.conf import settings


class Category(models.Model):
    """Food category for posts."""
    name = models.CharField(max_length=50, unique=True)
    emoji = models.CharField(max_length=5, blank=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return f'{self.emoji} {self.name}'.strip()


class Post(models.Model):
    """A food post shared by a user."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Usuario',
    )
    image = models.ImageField(
        upload_to='posts/%Y/%m/',
        verbose_name='Imagen',
    )
    caption = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Descripción',
    )
    food_name = models.CharField(
        max_length=100,
        verbose_name='Nombre del plato',
    )
    location = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Ubicación',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Categoría',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.food_name} por @{self.user.username}'

    def likes_count(self):
        return self.likes.count()

    def comments_count(self):
        return self.comments.count()

    def is_liked_by(self, user):
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()


class Like(models.Model):
    """A like on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='liked_posts',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f'@{self.user.username} → {self.post.food_name}'


class Comment(models.Model):
    """A comment on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(max_length=300, verbose_name='Comentario')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['created_at']

    def __str__(self):
        return f'@{self.user.username} en "{self.post.food_name}"'
