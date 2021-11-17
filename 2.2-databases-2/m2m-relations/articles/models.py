from django.db import models
from django.db.models import Q


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Scope(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    articles = models.ManyToManyField('Article', through='ArticleScopes')

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.title


class ArticleScopes(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='scopes')
    topic = models.ForeignKey(Scope, on_delete=models.CASCADE, verbose_name='Название темы')
    is_main = models.BooleanField(null=False, blank=False, verbose_name='Основная тема', default=False)

    class Meta:
        unique_together = ['article', 'topic']
        constraints = [
            models.UniqueConstraint(fields=['topic'], condition=Q(is_main=True), name='unique_main_topic')
        ]
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.topic.title