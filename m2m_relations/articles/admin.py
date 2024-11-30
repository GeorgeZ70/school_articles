from django.contrib import admin
from .models import Article, Scope, ArticleScope

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class ArticleScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_count = 0
        for form in self.forms:
            if form.cleaned_data['DELETE']:
                continue
            if form.cleaned_data['is_main']:
                is_main_count += 1
        if is_main_count > 1:
            raise ValidationError('Основным может быть только один раздел')
        if is_main_count < 1:
            raise ValidationError('Укажите основной раздел')
        return super().clean()  # вызываем базовый код переопределяемого метода


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    formset = ArticleScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at', 'image']

    @admin.display(description='Текст', ordering='text')
    def preview_text(self, obj: Article) -> str:
        return obj.text[:150]

    inlines = [ArticleScopeInline]
@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(ArticleScope)
class ArticleScopeAdmin(admin.ModelAdmin):
    list_display = ['id', 'scope', 'article', 'is_main']


