from django.contrib import admin
from django.utils.safestring import mark_safe 
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('get_image_preview', 'title', 'section', 'updated_at')  
    list_filter = ('section',)
    search_fields = ('title', 'content')
    
    readonly_fields = ('get_image_preview',)

    def get_image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="60" style="border-radius: 8px; border: 1px solid #334155;">')
        return "Без фото"
    get_image_preview.short_description = "Превью" 