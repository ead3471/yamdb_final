from django.contrib import admin
from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'name', 'description',
                    'category', 'get_genres')
    empty_value_display = '-пусто-'

    def get_genres(self, title: Title):
        return [genre.name for genre in title.genre.all()]


admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Category)
