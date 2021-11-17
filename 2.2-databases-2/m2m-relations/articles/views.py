
from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import Prefetch

from articles.models import Article, ArticleScopes


def articles_list(request):
    template = 'articles/news.html'
    context = {
        'object_list': list(Article.objects.prefetch_related(Prefetch(
                        'scopes',
                        queryset=ArticleScopes.objects.select_related('topic').order_by('-is_main', 'topic')))
                        .order_by('-published_at'))
    }
    return render(request, template, context)