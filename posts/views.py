
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.db.models import Q
from .models import Post
from .forms import CommentForm, PostForm  # <--- Make sure PostForm is here!
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    object_list = Post.objects.filter(status='published')
    
    # Show 3 posts per page (usually you do 10, but we use 3 since we have few posts)
    paginator = Paginator(object_list, 3) 
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'posts/list.html', {'posts': posts})



def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'posts/detail.html', 
    {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        
    })



def search(request):
    query = request.GET.get('q')
    results = [] # Fix indent
    if query:
        # Note the double underscore: title__icontains
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query),
            status='published'
        )
    # Note the plural: 'posts/search.html'
    return render(request, 'posts/search.html', {'query': query, 'results': results})



@login_required
def post_create(request):
    if request.method =='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            return redirect('posts:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html',{'form':form})