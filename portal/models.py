from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import re

class Article(models.Model):
    SECTION_CHOICES = [
        ('home', 'Главная страница'),
        ('theory', 'Теория'),
        ('news', 'Новости'), 
    ]
    
    IMAGE_POSITIONS = [
        ('top', 'Сверху (на всю ширину)'),
        ('left', 'Слева (обтекание)'),
        ('right', 'Справа (обтекание)'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    section = models.CharField(max_length=10, choices=SECTION_CHOICES, default='theory', verbose_name="Раздел")
    content = RichTextUploadingField(verbose_name="Текст статьи")
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Изображение")
    image_position = models.CharField(
        max_length=10, 
        choices=IMAGE_POSITIONS, 
        default='top', 
        verbose_name="Положение фото"
    )
    
    # Новое поле для ручного ввода времени
    reading_time = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        verbose_name="Время чтения (мин.)",
        help_text="Оставьте пустым для автоматического расчета"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['created_at'] 

    def get_reading_time(self):
        if self.reading_time:
            return self.reading_time
        
        # Алгоритм авторасчета
        clean_text = re.sub('<[^<]+?>', '', str(self.content))
        word_count = len(clean_text.split())
        minutes = round(word_count / 180)
        return minutes if minutes > 0 else 1

    def __str__(self):
        return f"{self.get_section_display()}: {self.title}"