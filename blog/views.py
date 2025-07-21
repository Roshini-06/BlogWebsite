from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, RegisterForm

# 🏠 Home Page (Requires Login)
@login_required
def post_list(request):
    query = request.GET.get("q")
    posts = Post.objects.all()
    if query:
        posts = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)
    return render(request, 'blog/post_list.html', {'posts': posts})


# 📄 Post Detail with Comments
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })


# ✨ Create New Post (Requires Login)
@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('post_list')
    return render(request, 'blog/post_form.html', {'form': form})


# 📝 Edit Existing Post (Author Only)
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("❌ You are not allowed to edit this post.")

    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_form.html', {'form': form})


# 🗑️ Delete Post (Author Only)
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("❌ You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        return render(request, 'blog/post_deleted.html')  # Create this template with "Post deleted. 🔙 Return home"

    return render(request, 'blog/post_confirm_delete.html', {'post': post})


# 👤 User Registration
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('post_list')
    return render(request, 'blog/register.html', {'form': form})
