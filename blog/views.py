from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


def post_index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    image_urls = []
    for post in posts:
        image_url = settings.STATIC_URL + str(post.author.profile.profile_pic)
        image_urls.append(image_url)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    post_image_list = zip(posts, image_urls)
    return render(request, "blog/post_index.html",
                  {"posts": posts, "page": page, "post_list": post_list, "post_image_list": post_image_list})


@login_required
def post_likes(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = post.comments.filter(approved_comment=True)
    liked_post = get_object_or_404(Post, pk=pk)
    num_of_likes = liked_post.num_of_likes()
    liked = False
    if liked_post.likes.filter(id=request.user.id).exists():
        liked = True
    else:
        liked = False
    from django.conf import settings

    image_url = settings.STATIC_URL + str(post.author.profile.profile_pic)
    return render(request, "blog/post_detail.html",
                  {"post": post, "comment": comment, "num_of_likes": num_of_likes, "liked": liked,
                   "image_url": image_url})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # these fields are required to be specific info.
            post.published_date = timezone.now()  # the user and time published shouldn't be chosen by the user.
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
        return render(request, "blog/post_create.html", {"form": form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, )
    if request.method == "POST" and post.author == request.user:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, "Post Successfully Updated!")
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, "blog/post_update.html", {"form": form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST" and post.author == request.user:
        post.delete()
        messages.success(request, "Post Successfully Deleted!")
        return redirect("post_index")
    else:
        return render(request, "blog/post_confirm_delete.html", {"post": post})


@login_required
def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(published_date__lte=timezone.now(), author=user).order_by("-published_date")
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    image_urls = []
    for post in posts:
        image_url = settings.STATIC_URL + str(post.author.profile.profile_pic)
        image_urls.append(image_url)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    post_image_list = zip(posts, image_urls)
    return render(request, "blog/user_posts.html",
                  {"posts": posts, "user": user, "post_image_list": post_image_list, "page": page})


@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.approved_comment = True
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, "blog/comment_create.html", {'form': form})
