from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    valid = False

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            if len(post.text) <= 5:
                valid = True
                return render(request, 'blog/post_edit.html', {'form': form, 'valid': valid})

            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form, 'valid': valid})

def post_edit(request, pk):
    valid = True
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid() and len(post.text) > 5:

            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            print(post.text)

            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)
        valid = False
        return render(request, 'blog/post_edit.html', {'form': form, 'valid': valid})

        #return render(request, 'blog/post_edit.html', {'form': form, 'valid': valid})

    return render(request, 'blog/post_edit.html', {'form': form, 'valid': valid})