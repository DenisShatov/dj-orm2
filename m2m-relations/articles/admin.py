from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, ArticleTags, Tag


class ArticleTagsInlineFormset(BaseInlineFormSet):
    def clean(self):
        checkbox = False

        for form in self.forms:
            if form.cleaned_data.get('is_main') and checkbox:
                raise ValidationError('Должен быть выбран только один основной раздел')
            if form.cleaned_data.get('is_main') and not checkbox:
                checkbox = True
        if checkbox is False:
            raise ValidationError('Необходимо выбрать основной раздел')

        return super().clean()


class ArticleTagsInline(admin.TabularInline):
    model = ArticleTags
    formset = ArticleTagsInlineFormset


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleTagsInline]
