from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, '¡Publicación creada con éxito! 🍽️')
            return redirect('posts:detail', pk=post.pk)
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('user', 'category'), pk=pk)
    comments = post.comments.select_related('user').order_by('created_at')
    comment_form = CommentForm()
    is_liked = post.is_liked_by(request.user)
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
    }
    return render(request, 'posts/detail.html', context)


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicación actualizada.')
            return redirect('posts:detail', pk=post.pk)
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit.html', {'form': form, 'post': post})


@login_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    post.delete()
    messages.success(request, 'Publicación eliminada.')
    return redirect('users:dashboard')


@login_required
@require_POST
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like_qs = Like.objects.filter(post=post, user=request.user)
    if like_qs.exists():
        like_qs.delete()
        liked = False
    else:
        Like.objects.create(post=post, user=request.user)
        liked = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': post.likes_count()})
    return redirect(request.META.get('HTTP_REFERER', 'feed:home'))


@login_required
@require_POST
def comment_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
    return redirect('posts:detail', pk=pk)


@login_required
@require_POST
def comment_delete(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, user=request.user)
    comment.delete()
    return redirect('posts:detail', pk=pk)
