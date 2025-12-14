from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.PostList.as_view(), name='post_list'),
    path('blog/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('blog/category/<str:slug>/', views.category_page, name='category_page'),
    path('blog/tag/<str:slug>/', views.tag_page, name='tag_page'),
    path('about_me/', views.about_me, name='about_me'),
]
