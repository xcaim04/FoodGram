from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.feed.urls')),
    path('auth/', include('apps.users.urls')),
    path('posts/', include('apps.posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
