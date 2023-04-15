from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'review', 'text', 'pub_date')
    search_fields = ('author', 'review')
    list_filter = ('author', 'review')
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Review)
class RevieweAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text', 'score', 'pub_date')
    search_fields = ('title', 'author', 'score', 'pub_date')
    list_filter = ('title', 'author', 'score', 'pub_date')
    empty_value_display = '-пусто-'


# @admin.register(Title)
# class TitleAdmin(admin.ModelAdmin):
#     list_display = ('name', 'year', 'get_genre', 'rating', 'category', 'description')
#     search_fields = ('name', 'year', 'category', 'get_genre', 'rating')
#     list_filter = ('name', 'year', 'genre', 'rating')
#     empty_value_display = '-пусто-'

#     def get_genre(self, obj):
#         return obj.get_genre
