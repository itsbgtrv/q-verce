from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Forum, News, Joblist
from .forms import PostForm, CommentForm, NewsForm
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse



def posts(request):
    # Берем все посты, свежие сверху
    all_posts = Post.objects.all().order_by('-created_at')
    sport_posts = Post.objects.filter(category__name='Спорт').order_by('-created_at')
    politics_posts = Post.objects.filter(category__name='Политика').order_by('-created_at')
    technology_posts = Post.objects.filter(category__name='Технологии').order_by('-created_at')

    
    
    # Распределяем посты по блокам для шаблона
    context = {
        # Первые 4 поста для верхнего ряда (REVIEWS)
        'strip_posts': all_posts[:4],
        # 5-й пост будет главным в блоке meddle_block_3_left
        'main_post': all_posts[5] if all_posts.count() > 5 else None,
        # Посты с 6-го по 10-й для правой колонки "Right Now"
        'right_now_posts': all_posts[6:11],

        'top_news_posts': all_posts[12:17],

        'strip_posts2': all_posts[18:22],

        'strip_posts3': sport_posts[:1],

        'strip_posts4': politics_posts[:1],
        
        'strip_posts5': technology_posts[:1],

        'strip_posts6': all_posts[23:24],

    }
    
    # Теперь мы ВСЕГДА рендерим base.html и передаем туда context
    return render(request, 'twitter_app/base.html', context)



def forum(request):

    if request.user.is_authenticated:
        forum_list = Forum.objects.all().order_by('-created_at')
        return render(request, 'twitter_app/forum.html', {'posts': forum_list})
    
    return render(request, 'twitter_app/checkverify.html')

def news(request):
    if request.user.is_authenticated:
        news_list = News.objects.all().order_by('-created_at')
        return render(request, 'twitter_app/news.html', {'posts': news_list})

    return render(request, 'twitter_app/checkverify.html')

def joblist(request):
    if request.user.is_authenticated:
        joblist_list = Joblist.objects.all().order_by('-created_at')
        return render(request, 'twitter_app/joblist.html', {'posts': joblist_list})
    
    return render(request, 'twitter_app/checkverify.html')

def checkverify(request):
    if request.user.is_authenticated:
        return render(request, 'twitter_app/home.html')
    
    return render(request, 'twitter_app/checkverify.html')

@login_required
def home_view(request):
    # Здесь показываем то, что должен видеть залогиненный юзер
    posts_list = Post.objects.all().order_by('-created_at')
    return render(request, 'twitter_app/posts.html', {'posts': posts_list})

def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('base') 
    else:
        post_form = PostForm()
    return render(request, 'twitter_app/create_post.html', {'post_form': post_form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': post.comments.all().order_by('-created_at'),
    }
    return render(request, 'twitter_app/post_detail.html', context)

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Проверка прав доступа: только автор может редактировать
    if request.user != post.user:
        return redirect('post_detail', pk=pk) # Или выкинуть 403

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'twitter_app/post_edit.html', {'form': form, 'post': post})


stripe.api_key = settings.STRIPE_SECRET_KEY

# Страница с карточками (твоя верстка)
def subscribe_page(request):
    return render(request, 'twitter_app/subscribe.html')

# Логика перехода на оплату
@login_required
def create_checkout_session(request):
    if request.method == 'POST':
        plan = request.POST.get('plan')
        # Замени эти ID на свои из Stripe Dashboard
        prices = {
            'annual': 'price_1...your_id', 
            'monthly': 'price_1...your_id',
        }
        
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                payment_method_types=['card'],
                line_items=[{'price': prices.get(plan), 'quantity': 1}],
                mode='subscription',
                success_url=request.build_absolute_uri('/') + '?success=true',
                cancel_url=request.build_absolute_uri('/subscribe/') + '?canceled=true',
                metadata={'user_id': request.user.id}
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return render(request, 'twitter_app/subscribe.html', {'error': str(e)})

    # ДОБАВЛЕНО: Если это GET запрос, просто отправляем пользователя на страницу выбора тарифа
    return redirect('subscribe') # Убедитесь, что 'subscribe' — это имя (name) вашего URL для страницы оплаты

# Вебхук, который "слушает" Stripe и выдает Premium в базу
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = "whsec_..." # Получишь в Stripe CLI или Dashboard

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        # Находим профиль и даем доступ
        from .models import Profile
        profile = Profile.objects.get(user_id=user_id)
        profile.is_premium = True
        profile.save()

    return HttpResponse(status=200)