from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import PostForm

def index(request):
	return render(request,'blogs/index.html')

@login_required
def posts(request):
	posts = BlogPost.objects.order_by('date_added')
	context = {'posts': posts}
	return render(request,'blogs/all_posts.html',context)

@login_required
def new_post(request):
	if request.method != 'POST':
		form = PostForm()
	else:
		form = PostForm(request.POST)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.owner = request.user
			new_post.save()
			return HttpResponseRedirect(reverse('blogs:posts'))

	context = {'form': form}
	return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
	post = BlogPost.objects.get(id=post_id)
	if post.owner != request.user:
		raise Http404
	if request.method != 'POST':
		form = PostForm(instance=post)
	else:
		form = PostForm(instance=post, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('blogs:posts'))

	context = {'post': post, 'form': form}
	return render(request,'blogs/edit_post.html', context)