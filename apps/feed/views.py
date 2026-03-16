from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.posts.models import Post, Category
from apps.users.models import Follow


def home(request):
    """
    Public/authenticated home.
    - Authenticated: show posts from followed users + own posts.
    - Anonymous: show all recent posts.
    """
    category_slug = request.GET.get('category')
    selected_category = None

    if request.user.is_authenticated:
        following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)
        user_ids = list(following_ids) + [request.user.email]
        posts = Post.objects.filter(user__email__in=user_ids).select_related(
            'user', 'category'
        ).prefetch_related('likes', 'comments')
        if not posts.exists():
            # fallback: show all posts if user follows nobody
            posts = Post.objects.select_related('user', 'category').prefetch_related('likes', 'comments')
    else:
        posts = Post.objects.select_related('user', 'category').prefetch_related('likes', 'comments')

    if category_slug:
        selected_category = Category.objects.filter(name__iexact=category_slug).first()
        if selected_category:
            posts = posts.filter(category=selected_category)

    posts = posts.order_by('-created_at')
    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'feed/home.html', context)


def explore(request):
    """Explore all posts, filterable by category."""
    category_slug = request.GET.get('category')
    selected_category = None

    posts = Post.objects.select_related('user', 'category').prefetch_related('likes', 'comments')

    if category_slug:
        selected_category = Category.objects.filter(name__iexact=category_slug).first()
        if selected_category:
            posts = posts.filter(category=selected_category)

    posts = posts.order_by('-created_at')
    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'feed/explore.html', context)
