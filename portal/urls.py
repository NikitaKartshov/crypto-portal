from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    
    # ТЕОРИЯ
    path('theory/', views.theory_list_view, name='theory'),
    path('article/<int:id>/', views.article_detail_view, name='article_detail'),
    path('theory/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:id>/edit/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:id>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    
    # ПРАКТИКА
    path('practice/', views.practice_list_view, name='practice'),
    path('practice/<int:id>/', views.practice_detail_view, name='practice_detail'),
    path('practice/create/', views.PracticeCreateView.as_view(), name='practice_create'),
    path('practice/<int:id>/edit/', views.PracticeUpdateView.as_view(), name='practice_update'),
    path('practice/<int:id>/delete/', views.PracticeDeleteView.as_view(), name='practice_delete'),
    
    # ИНСТРУМЕНТЫ
    path('tools/', views.tools_list_view, name='tools'),
    path('tools/<int:id>/', views.tool_detail_view, name='tool_detail'),
    path('tools/create/', views.ToolCreateView.as_view(), name='tool_create'),
    path('tools/<int:id>/edit/', views.ToolUpdateView.as_view(), name='tool_update'),
    path('tools/<int:id>/delete/', views.ToolDeleteView.as_view(), name='tool_delete'),
    
    # ПРОФИЛЬ И НАСТРОЙКИ
    path('settings/', views.settings_view, name='settings'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('update-theme/', views.update_theme, name='update_theme'), # ТА САМАЯ СТРОЧКА
    
    # АВТОРИЗАЦИЯ
    path('login/', views.auth_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
]