from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Forum, News, Joblist
from .forms import PostForm, CommentForm, NewsForm
from django.contrib.auth.decorators import login_required



def posts(request):
    # Берем все посты, свежие сверху
    all_posts = Post.objects.all().order_by('-created_at')
    
    # Распределяем посты по блокам для шаблона
    context = {
        # Первые 4 поста для верхнего ряда (REVIEWS)
        'strip_posts': all_posts[:4],
        # 5-й пост будет главным в блоке meddle_block_3_left
        'main_post': all_posts[4] if all_posts.count() > 4 else None,
        # Посты с 6-го по 10-й для правой колонки "Right Now"
        'right_now_posts': all_posts[5:10],
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

