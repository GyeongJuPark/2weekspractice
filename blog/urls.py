from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.PostList.as_view(), name='post_list'),
    path('blog/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('blog/create/', views.PostCreate.as_view(), name='post_create'),
    path('blog/<int:pk>/edit/', views.PostUpdate.as_view(), name='post_update'),
    path('blog/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('blog/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('blog/<int:pk>/comment/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),
    path('blog/category/<str:slug>/', views.category_page, name='category_page'),
    path('blog/tag/<str:slug>/', views.tag_page, name='tag_page'),
    path('blog/search/', views.search, name='search'),
    path('about_me/', views.about_me, name='about_me'),
]
