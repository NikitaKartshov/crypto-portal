from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from .models import UserProfile, Article, PracticeTask, CryptoTool

# Форма для управления статьями (теория)
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'image_position', 'section', 'visualizer_url']


# Форма для управления практическими заданиями
class PracticeForm(forms.ModelForm):
    class Meta:
        model = PracticeTask
        fields = [
            'title', 
            'description', 
            'task_text', 
            'correct_answer', 
            'hint', 
            'difficulty', 
            'related_article'
        ]


# Форма для инструментов (шифрование/дешифрование)
class ToolForm(forms.ModelForm):
    """Форма создания/редактирования криптографического инструмента"""
    class Meta:
        model = CryptoTool
        # Логика JS вынесена из БД в файлы для безопасности
        fields = ['title', 'description', 'tool_type', 'related_task']
        
        labels = {
            'title': 'Название инструмента',
            'description': 'Описание инструмента',
            'tool_type': 'Тип шифра (например: caesar, vigenere, atbash, playfair)',
            'related_task': 'Связанная задача (после решения которой инструмент разблокируется)',
        }
        
        help_texts = {
            'tool_type': 'Это значение используется для подключения соответствующего JS-файла. '
                         'Должно совпадать с именем файла в portal/static/portal/js/ciphers/',
        }


# Расширенная форма регистрации нового пользователя
class ExtendedRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    
    # Поле согласия с политикой конфиденциальности
    agree = forms.BooleanField(
        label=mark_safe(
            'Я согласен на <a href="/privacy/" class="privacy-link" target="_blank">обработку персональных данных</a>'
        ),
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


# Форма обновления основных данных аккаунта (User)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=False, max_length=30, label="Имя")
    last_name = forms.CharField(required=False, max_length=30, label="Фамилия")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# Форма обновления расширенного профиля пользователя (UserProfile)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'is_private']
        labels = {
            'avatar': 'Загрузить аватар',
            'is_private': 'Сделать профиль анонимным (скрыть имя и фамилию)'
        }


# Дополнительная настройка виджетов для формы инструментов
ToolForm.base_fields['tool_type'].widget.attrs.update({
    'placeholder': 'caesar, vigenere, atbash и т.д.'
})