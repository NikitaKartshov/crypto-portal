import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.utils import timezone

from .models import (
    UserProfile, Article, UserProgress,
    PracticeTask, UserPracticeProgress, CryptoTool
)
from .forms import (
    ArticleForm, PracticeForm, ToolForm,
    ExtendedRegisterForm, UserUpdateForm, ProfileUpdateForm
)

# --- Теория ---

def home_view(request):
    article = Article.objects.filter(section='home').first()
    return render(request, 'portal/index.html', {'article': article})

def theory_list_view(request):
    articles = Article.objects.filter(section='theory').order_by('id')
    completed_count = 0
    progress_percent = 0
    next_article = articles.first() if articles.exists() else None

    if request.user.is_authenticated:
        completed_ids = list(
            UserProgress.objects.filter(user=request.user)
            .values_list('article_id', flat=True)
        )
        completed_count = len(completed_ids)

        if articles.exists():
            progress_percent = int((completed_count / articles.count()) * 100)

        for article in articles:
            article.is_completed = article.id in completed_ids

        for article in articles:
            if not article.is_completed:
                next_article = article
                break

    return render(request, 'portal/theory.html', {
        'articles': articles,
        'completed_count': completed_count,
        'progress_percent': progress_percent,
        'next_article': next_article,
    })

def article_detail_view(request, id):
    article = get_object_or_404(Article, id=id)
    is_completed = False

    if request.user.is_authenticated:
        is_completed = UserProgress.objects.filter(
            user=request.user, article=article
        ).exists()

        if request.method == 'POST':
            if not is_completed:
                UserProgress.objects.create(user=request.user, article=article)
                messages.success(request, "Статья успешно изучена!")

                unlocked_task = PracticeTask.objects.filter(
                    related_article=article
                ).first()
                if unlocked_task:
                    messages.info(
                        request,
                        f"Открыто новое практическое задание: {unlocked_task.title}"
                    )
                    return redirect('practice_detail', id=unlocked_task.id)

            return redirect('theory')

    return render(request, 'portal/article_detail.html', {
        'article': article,
        'is_completed': is_completed,
    })

# --- Практика ---

def practice_list_view(request):
    tasks = PracticeTask.objects.all().order_by('id')
    completed_count = 0
    progress_percent = 0
    next_task = tasks.first() if tasks.exists() else None

    if request.user.is_authenticated:
        completed_task_ids = list(
            UserPracticeProgress.objects.filter(
                user=request.user, is_completed=True
            ).values_list('task_id', flat=True)
        )
        completed_article_ids = list(
            UserProgress.objects.filter(user=request.user)
            .values_list('article_id', flat=True)
        )

        completed_count = len(completed_task_ids)

        if tasks.exists():
            progress_percent = int((completed_count / tasks.count()) * 100)

        for task in tasks:
            task.is_completed = task.id in completed_task_ids
            task.is_available = (
                not task.related_article or
                task.related_article.id in completed_article_ids
            )

        for task in tasks:
            if task.is_available and not task.is_completed:
                next_task = task
                break
    else:
        for task in tasks:
            task.is_completed = False
            task.is_available = False

    for task in tasks:
        task.leaderboard = UserPracticeProgress.objects.filter(
            task=task, is_completed=True
        ).order_by('time_taken')[:3]

    return render(request, 'portal/practice.html', {
        'tasks': tasks,
        'completed_count': completed_count,
        'progress_percent': progress_percent,
        'next_task': next_task,
    })

def practice_detail_view(request, id):
    task = get_object_or_404(PracticeTask, id=id)

    if not request.user.is_authenticated:
        messages.error(request, "Войдите в аккаунт для доступа к заданиям.")
        return redirect('login')

    if task.related_article:
        has_theory = UserProgress.objects.filter(
            user=request.user, article=task.related_article
        ).exists()
        if not has_theory:
            messages.warning(
                request,
                f"Задание закрыто! Сначала изучите теорию: {task.related_article.title}"
            )
            return redirect('article_detail', id=task.related_article.id)

    progress, _ = UserPracticeProgress.objects.get_or_create(
        user=request.user,
        task=task
    )

    if progress.started_at is None:
        progress.started_at = timezone.now()
        progress.save()

    if request.method == 'POST':
        if progress.is_completed:
            messages.info(request, "Вы уже успешно решили это задание.")
            return redirect('practice')

        user_answer = request.POST.get('answer', '').strip()

        if user_answer.lower() == task.correct_answer.lower():
            progress.is_completed = True
            progress.completed_at = timezone.now()
            delta = progress.completed_at - progress.started_at
            progress.time_taken = max(0, int(delta.total_seconds()))
            progress.save()

            messages.success(
                request,
                f"Верно! Ваше время решения: {progress.get_formatted_time()}"
            )
            return redirect('practice')
        else:
            messages.error(request, "Неверный ответ. Попробуйте ещё раз.")

    return render(request, 'portal/practice_detail.html', {
        'task': task,
        'is_completed': progress.is_completed,
    })

# --- Инструменты ---

def tools_list_view(request):
    tools = CryptoTool.objects.all().order_by('id')

    if request.user.is_authenticated:
        completed_task_ids = list(
            UserPracticeProgress.objects.filter(
                user=request.user, is_completed=True
            ).values_list('task_id', flat=True)
        )
        for tool in tools:
            tool.is_available = (
                not tool.related_task or
                tool.related_task.id in completed_task_ids
            )
    else:
        for tool in tools:
            tool.is_available = False

    return render(request, 'portal/tools.html', {'tools': tools})

def tool_detail_view(request, id):
    tool = get_object_or_404(CryptoTool, id=id)

    if not request.user.is_authenticated:
        messages.error(request, "Войдите в аккаунт для доступа к инструментам.")
        return redirect('login')

    if tool.related_task:
        has_solved = UserPracticeProgress.objects.filter(
            user=request.user,
            task=tool.related_task,
            is_completed=True
        ).exists()
        if not has_solved:
            messages.warning(
                request,
                f"Инструмент закрыт! Сначала решите задачу: {tool.related_task.title}"
            )
            return redirect('practice_detail', id=tool.related_task.id)

    return render(request, 'portal/tool_detail.html', {'tool': tool})

# --- Аутентификация ---

def auth_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    login_form = AuthenticationForm()
    register_form = ExtendedRegisterForm()
    active_tab = 'login'

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'register':
            active_tab = 'register'
            register_form = ExtendedRegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, "Регистрация прошла успешно!")
                return redirect('home')

        elif action == 'login':
            active_tab = 'login'
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, "Вы успешно вошли в систему.")
                return redirect('home')

    return render(request, 'registration/login.html', {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': active_tab,
    })

def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect('home')

def profile_view(request, user_id):
    from django.contrib.auth.models import User
    target_user = get_object_or_404(User, id=user_id)
    return render(request, 'portal/profile.html', {'target_user': target_user})

# --- Настройки ---

@login_required
def settings_view(request):
    active_tab = request.GET.get('tab', 'profile')
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
            pass_form = PasswordChangeForm(request.user)

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Профиль успешно обновлён!')
                return redirect('/settings/?tab=profile')

        elif 'change_password' in request.POST:
            pass_form = PasswordChangeForm(request.user, request.POST)
            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменён!')
                return redirect('/settings/?tab=profile')

        elif 'theme' in request.POST:
            theme = request.POST.get('theme')
            if theme in ['dark', 'light']:
                user_profile.theme = theme
                user_profile.save()
                return redirect('/settings/?tab=site')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_profile)
        pass_form = PasswordChangeForm(request.user)

    return render(request, 'portal/settings.html', {
        'u_form': u_form,
        'p_form': p_form,
        'pass_form': pass_form,
        'active_tab': active_tab,
    })

@login_required
def update_theme(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            theme = data.get('theme')
            if theme in ['light', 'dark']:
                profile = request.user.profile
                profile.theme = theme
                profile.save()
                return JsonResponse({'status': 'ok', 'theme': theme})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error'}, status=400)

# --- Дополнительно ---

def privacy_policy(request):
    return render(request, 'portal/privacy_policy.html')

# --- Административные классы ---

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class ArticleCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'portal/article_form.html'
    success_url = reverse_lazy('theory')

class ArticleUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'portal/article_form.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'id': self.object.id})

class ArticleDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Article
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('theory')

class PracticeCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = PracticeTask
    form_class = PracticeForm
    template_name = 'portal/practice_form.html'
    success_url = reverse_lazy('practice')

class PracticeUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = PracticeTask
    form_class = PracticeForm
    template_name = 'portal/practice_form.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy('practice_detail', kwargs={'id': self.object.id})

class PracticeDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = PracticeTask
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('practice')

class ToolCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = CryptoTool
    form_class = ToolForm
    template_name = 'portal/tool_form.html'
    success_url = reverse_lazy('tools')

class ToolUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = CryptoTool
    form_class = ToolForm
    template_name = 'portal/tool_form.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse_lazy('tool_detail', kwargs={'id': self.object.id})

class ToolDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = CryptoTool
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('tools')