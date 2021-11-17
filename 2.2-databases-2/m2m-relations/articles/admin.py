from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, ArticleScopes


class ArticleScopesInlineFormset(BaseInlineFormSet):

    @staticmethod
    def error(err):
        raise ValidationError(err)

    def clean(self):

        main_in_form = False
        delete_main = False
        err = None
        n = 0

        for form in self.forms:
            main = form.cleaned_data.get('is_main')
            delete = form.cleaned_data.get('DELETE')

            if main and delete:
                if not main_in_form and n > 0:
                    err = 'Назначьте другую тему основной перед удалением.'
                else:
                    main_in_form = True
                    delete_main = True
            elif main and not delete:
                if main_in_form and not delete_main:
                    err = 'Статья может иметь только одну основную тему.'
                else:
                    main_in_form = True
            if main_in_form and delete and delete_main and n > 0:
                err = 'Нельзя удалить все основные темы.'
            if not main and not main_in_form:
                err = 'Статья может иметь только одну основную тему.'

            if err:
                self.error(err)
            else:
                n += 1

        return err


class ArticleScopesInline(admin.TabularInline):
    model = ArticleScopes
    formset = ArticleScopesInlineFormset


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    model = Scope


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleScopesInline]