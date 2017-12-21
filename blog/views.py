from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse, redirect
from .models import Article, Comment, UserProfile
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import markdown


# _LABEL_COLOR = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple']
# UniformMetaData.article_all = Article.objects.order_by('-created_at')

# # make sure labels is unique in template
# def labels():
#     labels = set()
#     for article in UniformMetaData.article_all:
#         labels.add(article.label)
#     return sample(labels,15)
#
#
# def created_date():
#     created_date = set()
#     for article in UniformMetaData.article_all:
#         dt = article.created_at.strftime('%Y-%m')
#         created_date.add(dt)
#     return created_date

#
class UniformMetaData(object):
    label_color = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple']

    @classmethod
    def article_all(cls):
        article_all = Article.objects.order_by('-id')
        return article_all

    @classmethod
    def label(cls):
        labels = set()
        for article in cls.article_all():
            if article.label.strip():
                labels.add(article.label.strip())
        print(labels)
        # if len(labels) > 15:
        #     return random.sample(labels, 15)
        # else:
        return labels

    @classmethod
    def created_date(cls):
        created_date = set()
        for article in cls.article_all():
            dt = article.created_at.strftime('%Y-%m')
            created_date.add(dt)
        return created_date


# 本来写了好几段的重复代码，这里取相同的变量article——list就好了，不用重复写渲染的代码了
def article(request, article_set=None, article_date=None):
    if article_set:
        article_list = get_list_or_404(Article, label=article_set)
        # print('article_set ======================= ' , article_list)

    elif article_date:
        article_list = []
        for article in UniformMetaData.article_all():
            if article.created_at.strftime('%Y-%m') == article_date:
                article_list.append(article)
                # print('article_cate ======================= ' , article_list)
    else:
        article_list = UniformMetaData.article_all()
        # print('article_all ======================= ', article_list)
    # print(article_list)
    # articles已经变成page对象,不再是普通的变量
    paginator = Paginator(article_list, 5)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    except PageNotAnInteger:  # 如果get到none则捕捉此错误
        articles = paginator.page(1)
    # print('article in page ==========', articles)
    for article in articles:
        article.content = markdown.markdown(article.content,
                                            extensions=[
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc',
                                            ])
    return render(request, 'blog/blog.html', {'articles': articles,
                                              'labels': UniformMetaData.label(),
                                              'label_color': UniformMetaData.label_color,
                                              'article_all': UniformMetaData.article_all(),
                                              'article_filter_by_month': UniformMetaData.created_date(),
                                              }
                  )


def article_detail(request, article_id, err_form=None):
    article = get_object_or_404(Article, pk=article_id)
    article.content = markdown.markdown(article.content,
                                        extensions=[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.toc',
                                        ])
    comment_list = article.comment_set.order_by('-created_at')
    if err_form:
        comment_form = err_form
    else:
        comment_form = CommentForm
    # if request.method == 'POST':
    #     comment_form = CommentForm(request.POST)  # 绑定表单
    #     if comment_form.is_valid():  # 没有此行,校验依然可行,添加此行只是为了逻辑判断
    #         comment_content = comment_form.cleaned_data['comment_content']
    #         comment = Comment(article=article,content=comment_content)
    #         comment.save()
    #         return HttpResponseRedirect(reverse('blog:article', args=[article.id, ]))  # 记得return
    return render(request, 'blog/article.html', {'article': article,
                                                 'label_color': UniformMetaData.label_color,
                                                 'labels': UniformMetaData.label(),
                                                 'article_all': UniformMetaData.article_all(),
                                                 'article_filter_by_month': UniformMetaData.created_date(),
                                                 'comment_form': comment_form,
                                                 'comment_list': comment_list,
                                                 }
                  )


@login_required(login_url='blog:login')
def article_detail_comment(request, article_id):
    comment_form = CommentForm(request.POST)  # 绑定表单
    # if not authenticate(request.user):
    #     redirect(to=)

    if comment_form.is_valid():  # 没有此行,校验依然可行,添加此行只是为了逻辑判断
        article = Article.objects.get(pk=article_id)
        comment_content = comment_form.cleaned_data['comment_content']
        comment = Comment(article=article, content=comment_content, author=request.user)
        comment.save()
        return HttpResponseRedirect(reverse('blog:article', args=(article.id,)))
    else:
        return article_detail(request, article_id, err_form=comment_form)  # view内传递数据依然可以传递表单错误信息，而直接重定向则失效


def blog_login(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'GET':
        form = AuthenticationForm
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/blog')
    context = {}
    context['form'] = form
    context['next'] = redirect_to
    return render(request, 'blog/register_login.html', context)


def blog_register(request):
    if request.user.is_authenticated:
        logout(request)
    context = {}
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'GET':
        form = UserCreationForm
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                                )
            avatar = request.FILES.get('avatar')  # 注意这里是files
            userprofile = UserProfile(belong_to=user, profile_image=avatar)
            userprofile.save()
            login(request, user)
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('blog:article_list')
    context['form'] = form
    context['next'] = redirect_to
    return render(request, 'blog/register_login.html', context)
