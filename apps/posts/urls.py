from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.post_create, name='create'),
    path('<int:pk>/', views.post_detail, name='detail'),
    path('<int:pk>/edit/', views.post_edit, name='edit'),
    path('<int:pk>/delete/', views.post_delete, name='delete'),
    path('<int:pk>/like/', views.like_toggle, name='like'),
    path('<int:pk>/comment/', views.comment_add, name='comment_add'),
    path('<int:pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
]
