from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name='base'), # Это главная: либо лендинг, либо лента
    path('home/', views.home_view, name='home'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('forum/', views.forum, name='forum'),
    path('news/', views.news, name='news'),
    path('joblist/', views.joblist, name='joblist'),
    path('verify/', views.checkverify, name='checkverify'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('subscribe/', views.subscribe_page, name='subscribe'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
]