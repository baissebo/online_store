from autoslug import AutoSlugField
from django.db import models

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование категории")
    description = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование товара")
    description = models.TextField(verbose_name="Описание товара")
    image = models.ImageField(
        upload_to="product/img", verbose_name="Превью товара", **NULLABLE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        **NULLABLE,
        related_name="products"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name", "category"]


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя контакта")
    email = models.EmailField()
    message = models.TextField(verbose_name="Сообщение пользователя")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ['-created_at']


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок поста")
    slug = models.CharField(unique=True, verbose_name="Ссылка для поста")
    content = models.TextField(verbose_name="Текст поста")
    preview_image = models.ImageField(upload_to="blog_preview", verbose_name="Превью поста", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликованные посты")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-created_at']
