from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Article

def home_view(request):
    article = Article.objects.filter(section='home').first()
    return render(request, 'portal/index.html', {'article': article})

def theory_list_view(request):
    articles = Article.objects.filter(section='theory')
    return render(request, 'portal/theory.html', {'articles': articles})

def article_detail_view(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'portal/article_detail.html', {
        'article': article
    })

def practice_view(request):
    return render(request, 'portal/practice.html')

def tools_view(request):
    return render(request, 'portal/tools.html')

def auth_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    active_tab = 'login'
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'register':
            active_tab = 'register'
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('home')
        elif action == 'login':
            active_tab = 'login'
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Неверный логин или пароль.")
    return render(request, 'registration/login.html', {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': active_tab
    })

def logout_view(request):
    logout(request)
    return redirect('home')

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class ArticleCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Article
    template_name = 'portal/article_form.html'
    fields = ['title', 'content', 'image', 'image_position', 'section', 'reading_time']
    success_url = reverse_lazy('theory')

    def form_valid(self, form):
        if not form.cleaned_data.get('section'):
            form.instance.section = 'theory'
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Article
    template_name = 'portal/article_form.html'
    fields = ['title', 'content', 'image', 'image_position', 'section', 'reading_time']
    
    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'id': self.object.id})

class ArticleDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('theory')