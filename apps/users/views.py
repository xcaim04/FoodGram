from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from .forms import RegisterForm, LoginForm, ProfileEditForm, ChangePasswordForm
from .models import User, Follow


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('feed:home')
        return render(request, self.template_name, {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido a FoodGram, @{user.username}!')
            return redirect('feed:home')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('feed:home')
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get('next', 'feed:home')
            return redirect(next_url)
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('users:login')


class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, username):
        profile_user = get_object_or_404(User, username=username)
        posts = profile_user.posts.select_related('user').prefetch_related('likes').order_by('-created_at')
        is_following = False
        if request.user.is_authenticated:
            is_following = Follow.objects.filter(
                follower=request.user, following=profile_user
            ).exists()
        context = {
            'profile_user': profile_user,
            'posts': posts,
            'is_following': is_following,
            'is_own_profile': request.user == profile_user,
        }
        return render(request, self.template_name, context)


class FollowToggleView(View):
    @login_required
    def post(self, request, username):
        target = get_object_or_404(User, username=username)
        if target == request.user:
            messages.error(request, 'No puedes seguirte a ti mismo.')
            return redirect('users:profile', username=username)
        follow_qs = Follow.objects.filter(follower=request.user, following=target)
        if follow_qs.exists():
            follow_qs.delete()
            messages.info(request, f'Dejaste de seguir a @{username}.')
        else:
            Follow.objects.create(follower=request.user, following=target)
            messages.success(request, f'Ahora sigues a @{username}.')
        return redirect('users:profile', username=username)


@login_required
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        messages.error(request, 'No puedes seguirte a ti mismo.')
        return redirect('users:profile', username=username)
    follow_qs = Follow.objects.filter(follower=request.user, following=target)
    if follow_qs.exists():
        follow_qs.delete()
    else:
        Follow.objects.create(follower=request.user, following=target)
    return redirect('users:profile', username=username)


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    user = request.user
    posts = user.posts.order_by('-created_at')
    context = {
        'posts': posts,
        'section': 'posts',
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def dashboard_settings(request):
    profile_form = ProfileEditForm(instance=request.user)
    password_form = ChangePasswordForm(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'profile':
            profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Perfil actualizado correctamente.')
                return redirect('users:dashboard_settings')
            else:
                messages.error(request, 'Corrige los errores del formulario.')

        elif action == 'password':
            password_form = ChangePasswordForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                from django.contrib.auth import update_session_auth_hash
                password_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Contraseña cambiada correctamente.')
                return redirect('users:dashboard_settings')
            else:
                messages.error(request, 'Corrige los errores del formulario.')

    return render(request, 'dashboard/settings.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'section': 'settings',
    })
