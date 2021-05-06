from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.views.generic import ListView

from .models import BlogPost
from .forms import BlogForm
from django.http import Http404

# Helper function
def check_blogpost_owner(blogpost, request):
    """# Make sure the topic belongs to the current user."""
    if blogpost.owner != request.user:
        raise Http404

# Create your views here.

def index(request):
    """The home page for blogs."""
    return render(request, 'blogs/index.html')

def entries(request):
    """The home page for viewing blogs.  Show all blog posts"""
    blogposts = BlogPost.objects.order_by('date_added')
    context = {'blogposts': blogposts}
    return render(request, 'blogs/entries.html', context)

@login_required
def new_blogpost(request):
    """Add new blogpost."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = BlogForm()
    else:
        # POST data submitted; process data.
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blogpost = form.save(commit=False)
            new_blogpost.owner = request.user
            new_blogpost.save()
            return redirect('blogs:entries')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_blogpost.html', context)

@login_required
def edit_blogpost(request, blogpost_id):
    """Edit existing blogpost"""
    blogpost = get_object_or_404(BlogPost, id=blogpost_id)
    check_blogpost_owner(blogpost, request)

    if request.method != 'POST':
        # Inital request; pre-fill form with current entry.
        form = BlogForm(instance=blogpost)
    else:
        # Post data submitted; process data.
        form = BlogForm(instance=blogpost, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:entries')

    context = {'blogpost': blogpost, 'form': form}
    return render(request, 'blogs/edit_blogpost.html', context)

class SearchResultsView(ListView):
    model = BlogPost
    template_name = 'blogs/search_results.html'    

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = BlogPost.objects.annotate(
            search=SearchVector('title', 'text', 'owner'),
            ).filter(search=query)
        return object_list