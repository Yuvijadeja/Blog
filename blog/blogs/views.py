import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Blogs

# Create your views here.


def cat_load():
    cat_design = Blogs.objects.filter(category="Designing").count()
    cat_script_lang = Blogs.objects.filter(category="Scripting-Language").count()
    cat_pro_lang = Blogs.objects.filter(category="Programming-Language").count()
    cat_tech = Blogs.objects.filter(category="Technology").count()
    cat_pro = Blogs.objects.filter(category="Programming").count()
    categories = [cat_design, cat_script_lang, cat_pro_lang, cat_tech, cat_pro]
    return categories


def home(request):
    blogs = Blogs.objects.all()

    if not blogs:
        messages.info(request, "No records found!")
        return render(request, 'home.html', {'categories': cat_load()})
    else:
        page = request.GET.get('page', 1)
        paginator = Paginator(blogs, 3)
        try:
            blog = paginator.page(page)
        except PageNotAnInteger:
            blog = paginator.page(1)
        except EmptyPage:
            blog = paginator.page(paginator.num_pages)
        return render(request, 'home.html', {'blogs': blog, 'categories': cat_load()})


def articles(request, filter_blog="all"):
    search = request.GET.get('search', "all")

    if filter_blog == "title" and search != "all":
        blogs = Blogs.objects.filter(title__contains=search).all()
    elif filter_blog == "category" and search != "all":
        blogs = Blogs.objects.filter(category__contains=search).all()
    elif filter_blog == "creator" and search != "all":
        blogs = Blogs.objects.filter(creator=search).all()
    else:
        blogs = Blogs.objects.all()

    if not blogs:
        messages.info(request, "No records found!")
        return render(request, 'articles.html', {'categories': cat_load()})
    else:
        page = request.GET.get('page', 1)
        paginator = Paginator(blogs, 3)
        try:
            blog = paginator.page(page)
        except PageNotAnInteger:
            blog = paginator.page(1)
        except EmptyPage:
            blog = paginator.page(paginator.num_pages)
        return render(request, 'articles.html', {'blogs': blog, 'categories': cat_load(),
                                                 'search': search, 'filterBy': filter_blog})


def blog_detail(request, blog_id):
    blog = Blogs.objects.get(id=blog_id)
    return render(request, 'blog-detail.html', {'categories': cat_load(), 'blog': blog})


def blog_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST.get("blogTitle")
            category = request.POST.get("category")
            image = request.FILES["blogImg"]
            desc = request.POST.get("desc")
            date = datetime.datetime.now()
            creator = request.user.username

            blog = Blogs.objects.create(title=title, category=category, img=image, description=desc, date=date, creator=creator)
            blog.save()
            messages.info(request, "Blog created successfully!")
            return redirect('blog-post')
        else:
            return render(request, 'blog-post.html', {'categories': cat_load()})
    else:
        return redirect('login')


def delete_blog(request, blog_id):
    if request.user.is_authenticated:
        Blogs.objects.filter(id=blog_id).delete()
        return redirect('account')
    else:
        return redirect('login')
