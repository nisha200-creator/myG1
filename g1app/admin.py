# from django.contrib import admin
# from .models import Article

# @admin.register(Article)
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'is_featured', 'created_at')
#     list_filter = ('category', 'is_featured')
#     search_fields = ('title', 'subtitle', 'content')



from django.contrib import admin
from .models import Article, Video, Race, RaceResult


# --------------------------
# ARTICLE ADMIN
# --------------------------
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'subtitle', 'content')

    fields = (
        'title',
        'slug',          # ✅ ADD THIS LINE
        'subtitle',
        'content',
        'category',
        'thumbnail',
        'video',
        'is_featured',
        'created_at',
    )

    prepopulated_fields = {'slug': ('title',)}   # ✅ Auto-generate slug in admin




# --------------------------
# VIDEO ADMIN
# --------------------------
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)


# --------------------------
# RACE (SCHEDULE) ADMIN
# --------------------------
@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('round_number', 'name', 'date_range')
    ordering = ('round_number',)
    search_fields = ('name',)


# --------------------------
# RACE RESULT ADMIN
# --------------------------
@admin.register(RaceResult)
class RaceResultAdmin(admin.ModelAdmin):
    list_display = ('grand_prix', 'date', 'winner', 'team', 'laps', 'time')
    list_filter = ('team', 'winner')
    search_fields = ('grand_prix', 'winner', 'team')
    ordering = ('date',)




# subscribe
from .models import Subscriber

admin.site.register(Subscriber)