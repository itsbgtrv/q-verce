from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse  # Добавили импорт

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-псевдоним")
    description = models.TextField(max_length=300, blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='New Post')
    content = models.TextField(max_length=350)
    subtitle = models.TextField(max_length=100, default='', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)
    is_trending = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Добавил fallback на случай пустого имени
        name = self.user.first_name or self.user.username
        return f'{name} - {self.title}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=150)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name}: {self.text[:30]}'

class Forum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='forum_posts') 
    text = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

class News(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=150)
    title = models.CharField(max_length=100, default="Без названия")

class Joblist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    text = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)


# Добавь в конец models.py
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Профиль: {self.user.username}"

# Автоматическое создание профиля при регистрации юзера
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)