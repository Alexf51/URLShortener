from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('urls/', views.url_list, name='url_list'),
    path('list/ajax/', views.url_list_ajax, name='url_list_ajax'),
    path('urls/create/', views.create_url, name='create_url'),
    path('urls/<pk>/', views.url_detail, name='url_detail'),
    path('user/', views.user_list, name='user_list'),
    path('users/<pk>/', views.user_detail, name='user_detail'),
    path('last_redirects/', views.last_redirects, name='last_redirects'),
    path('<str:short_url>/', views.redirect_to_original_url, name='redirect_to_original'),
    path('admin/', views.admin_custom_index, name='admin_custom_index'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]