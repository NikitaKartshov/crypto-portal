from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('theory/', views.theory_list_view, name='theory'),
    path('practice/', views.practice_view, name='practice'),
    path('tools/', views.tools_view, name='tools'),
    path('login/', views.auth_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('article/<int:id>/', views.article_detail_view, name='article_detail'),
    path('theory/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]