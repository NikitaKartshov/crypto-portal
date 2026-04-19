from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import re
from django.db.models.signals import post_save
from django.dispatch import receiver


# Проверка, чтобы картинка не весила слишком много
def validate_image_size(file):
    if file.size > 5 * 1024 * 1024:
        raise ValidationError('Изображение не должно превышать 5 МБ.')


# Модель для статей (Теория, Новости и Главная)
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
    section = models.CharField(
        max_length=10,
        choices=SECTION_CHOICES,
        default='theory',
        verbose_name="Раздел"
    )
    content = models.TextField(verbose_name="Текст статьи")
    
    image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        verbose_name="Изображение",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp']),
            validate_image_size,
        ]
    )
    
    image_position = models.CharField(
        max_length=10,
        choices=IMAGE_POSITIONS,
        default='top',
        verbose_name="Положение фото"
    )
    
    visualizer_url = models.URLField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name="Ссылка на визуализатор"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['id']

    # Считаем, сколько минут уйдет на чтение текста
    def get_reading_time(self):
        clean_text = re.sub('<[^<]+?>', '', str(self.content))
        word_count = len(clean_text.split())
        minutes = round(word_count / 90)
        return minutes if minutes > 0 else 1

    def __str__(self):
        return f"{self.get_section_display()}: {self.title}"


# Храним данные о том, какие статьи прочитал пользователь
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Статья")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата завершения")

    class Meta:
        unique_together = ('user', 'article')
        verbose_name = "Прогресс по статье"
        verbose_name_plural = "Прогресс по статьям"

    def __str__(self):
        return f"{self.user.username} — {self.article.title}"


# Модель для практических задач и упражнений
class PracticeTask(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]

    title = models.CharField(max_length=200, verbose_name="Заголовок задания")
    description = models.TextField(verbose_name="Описание")
    task_text = models.TextField(verbose_name="Текст задания (шифровка)")
    correct_answer = models.CharField(max_length=200, verbose_name="Правильный ответ")
    hint = models.TextField(blank=True, null=True, verbose_name="Подсказка")
    
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy',
        verbose_name="Сложность"
    )
    
    related_article = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная статья"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Практическое задание"
        verbose_name_plural = "Практические задания"
        ordering = ['id']

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.title}"


# Отслеживаем решение задач: время начала, конца и результат
class UserPracticeProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    task = models.ForeignKey(PracticeTask, on_delete=models.CASCADE, verbose_name="Задание")

    started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Время начала решения"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Время завершения"
    )
    
    is_completed = models.BooleanField(default=False, verbose_name="Решено")
    time_taken = models.IntegerField(null=True, blank=True, verbose_name="Затрачено секунд")

    class Meta:
        unique_together = ('user', 'task')
        ordering = ['time_taken']
        verbose_name = "Прогресс по заданию"
        verbose_name_plural = "Прогресс по заданиям"

    # Красивый вывод времени (минуты и секунды)
    def get_formatted_time(self):
        if self.time_taken is None:
            return "—"
        minutes, seconds = divmod(self.time_taken, 60)
        if minutes > 0:
            return f"{minutes} мин {seconds} сек"
        return f"{seconds} сек"

    def __str__(self):
        status = 'Решено' if self.is_completed else 'В процессе'
        return f"{self.user.username} — {self.task.title} ({status})"


# Инструменты криптографии (шифраторы/дешифраторы на JS)
class CryptoTool(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название инструмента")
    description = models.TextField(verbose_name="Описание")
    
    tool_type = models.CharField(
        max_length=50,
        verbose_name="Тип шифра",
        help_text="Например: caesar, vigenere, atbash"
    )
    
    related_task = models.ForeignKey(
        PracticeTask,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная задача (для разблокировки)"
    )

    class Meta:
        verbose_name = "Криптографический инструмент"
        verbose_name_plural = "Криптографические инструменты"

    def __str__(self):
        return self.title

    # Путь к файлу с логикой шифра
    def get_js_file(self):
        return f"portal/js/ciphers/{self.tool_type}.js"


# Дополнительные данные пользователя (аватар, тема, ФИО)
class UserProfile(models.Model):
    THEME_CHOICES = [
        ('dark', 'Темная'),
        ('light', 'Светлая'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Пользователь"
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Аватар",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp']),
            validate_image_size,
        ]
    )
    
    full_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Полное ФИО"
    )
    
    theme = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='dark',
        verbose_name="Тема сайта"
    )
    
    is_private = models.BooleanField(
        default=False,
        verbose_name="Приватный профиль"
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"


# Автоматическое создание профиля, когда создается новый User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


# Авто-сохранение профиля при сохранении User
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()