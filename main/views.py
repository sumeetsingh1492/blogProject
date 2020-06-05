from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Blog, BlogCategory, BlogSeries
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def single_slug(request, single_slug):
    # first check to see if the url is in categories.

    categories = [c.category_slug for c in BlogCategory.objects.all()]
    if single_slug in categories:
        matching_series = BlogSeries.objects.filter(blog_category__category_slug=single_slug)
        series_urls = {}

        for m in matching_series.all():
            part_one = Blog.objects.filter(blog_series__blog_series=m.blog_series).earliest("blog_published")
            series_urls[m] = part_one.blog_slug

        return render(request=request,
                      template_name='main/category.html',
                      context={"blog_series": matching_series, "part_ones": series_urls})

    blogs = [t.blog_slug for t in Blog.objects.all()]

    if single_slug in blogs:
        this_blog = Blog.objects.get(blog_slug=single_slug)
        blogs_from_series = Blog.objects.filter(blog_series__blog_series=this_blog.blog_series).order_by('blog_published')
        this_blog_idx = list(blogs_from_series).index(this_blog)

        return render(request=request,
                      template_name='main/blog.html',
                      context={"blog": this_blog,
                               "sidebar": blogs_from_series,
                               "this_tut_idx": this_blog_idx})




def homepage(request):
    return render(request = request,
                  template_name='main/categories.html',
                  context = {"categories":BlogCategory.objects.all})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            messages.success(request, f"You are now loggein in as {username}")
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")
