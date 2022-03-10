from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from .models import Post, Comment
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, get_user_model
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.db.models import Q
from taggit.models import Tag
from django.contrib.messages import *

# Create your views here.
def index(request):
    return render(request, 'blog/index.html')


def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 6)  # будет по 6 постов на одной странице
    page_number = request.GET.get('page')  #
    print("PN=", page_number)

    page_object = paginator.get_page(page_number)
    return render(request, 'blog/home.html', context={'page_object': page_object})


def contact(request):
    if request.method == 'GET':
        form = FeedbackForm()
        return render(request, 'blog/contact.html', context={'form': form})
    elif request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {subject}', message, email, [str(settings.EMAIL_HOST_USER)])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect(reverse('blog-contactthanks'))
        return render(request, 'blog/contact.html', context={'form': form})


def contactthanks(request):
    return render(request, 'blog/contact_thanks.html', {'title': 'Спасибо'})


def search(request):
    return render(request, 'blog/search.html', context={
        'title': 'Поиск'
    })


def search_results(request):
    query = request.GET.get('q')  # вытаскиваем из поисковой строки запрос
    results = ""
    results2= ""
    if query:
        # ищем по всем записям, а точнее их элементам h1 и content
        #print(Post.objects.filter())
        results = Post.objects.filter(Q(h1__icontains=query) | Q(content__icontains=query) | Q(tag__name__contains=query))
        #print("tag=", tag__)
    paginator = Paginator(results, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/search_results.html', context={
        'title': 'Поиск',
        'page_object': page_obj,
        'count': paginator.count
    })


def signin(request):
    if request.method == 'GET':
        form = SignInForm()
        return render(request, 'blog/sign_in.html', context={'form': form})
    elif request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'blog/sign_in.html', context={'form': form})


def signup(request):
    alert = False
    if request.method == 'GET':
        form = SignupForm()
        return render(request, 'blog/sign_up.html', context={'form': form, 'alert':alert})
    elif request.method == 'POST':
        form = SignupForm(request.POST)
        print("UA ", User.objects.all())

        users = get_user_model().objects.all()
        print('fc ', users)
        if form.is_valid():  # проверка всех введённых данных в формы
            user = form.save()
            if user is not None:
                login(request, user)
                alert = True
                success(request, 'User has been registered successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'blog/sign_up.html', context={'form': form, 'alert':alert})


def record(request, url_slug: str):
    # Было
    # post = get_object_or_404(Post, url_slug=url_slug)
    # common_tags = Post.tag.most_common()
    # last_posts = Post.objects.all().order_by('-id')[:5]
    # return render(request, 'blog/blog_record.html', context={
    #     'post': post,
    #     'common_tags':common_tags,
    #     'last_posts':last_posts
    # })
    if request.method == 'GET':
        post = get_object_or_404(Post, url_slug=url_slug)
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-id')[:5]
        comment_form = CommentForm()
        return render(request, 'blog/blog_record.html', context={
            'post':post,
            'common_tags':common_tags,
            'last_posts':last_posts,
            'comment_form':comment_form
        })
    elif request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            username = request.user
            post = get_object_or_404(Post, url_slug=url_slug)
            comment = Comment.objects.create(post=post, username=username, text=text)
            # редирект на страницу, на которой пользователь находился до отправки комментария
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, 'blog/blog_record.html', context={'comment_form':comment_form})

def tag(request, slug: str):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tag=tag)
    common_tags = Post.tag.most_common()
    # common_tags = [str(i) for i in Post.tag.most_common()]
    # print(common_tags)
    return render(request, 'blog/tag.html', context={
        'title': f'#ТЕГ {tag}',
        'posts': posts,
        'common_tags': common_tags
    })