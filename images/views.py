from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings

from common.decorators import Ajax_required
from actions.utils import create_action
from .forms import ImageCreationForm
from .models import Image
import redis


r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DF)
# Create your views here.

def image_create(request):
    if request.method == 'POST':

        form = ImageCreationForm(data=request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully')

            return redirect(new_item.get_absolute_url())

    else:
        form = ImageCreationForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  {'form': form,
                   'section': 'images'})



def image_detail(request, id, slug):
    '''returning a details page view for each image'''
    image = get_object_or_404(Image, id=id, slug=slug)
    # Increment image view by one
    total_views = r.incr('image:{}:view'.format(image.id))
    return render(request, 'images/image/detail.html',
                  {'image': image,
                   'section': 'images',
                   'total_views': total_views})

@Ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
                create_action(request.user, 'like image', image)
            else:
                image.user_like.remove(request.user)
                create_action(request.user, 'unlike image', image)

            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def image_list(request):
   images = Image.objects.all()
   paginator = Paginator(images, 8)
   page = request.GET.get('page')
   try:
       images = paginator.page(page)
   except PageNotAnInteger:
       # If page is not an integer deliver the first page
       images = paginator.page(1)
   except EmptyPage:
       if request.is_ajax():
           # If the request is AJAX and the page is out of range
           # return an empty page
           return HttpResponse('')
       # If page is out of range deliver last page of results
       images = paginator.page(paginator.num_pages)
   if request.is_ajax():
       return render(request,
                     'images/image/list_ajax.html',
                     {'section': 'images', 'images': images})
   return render(request,
                 'images/image/list.html',
                  {'section': 'images', 'images': images})