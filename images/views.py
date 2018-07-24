from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from common.decorators import Ajax_required
from .forms import ImageCreationForm
from .models import Image


# Create your views here.

def image_create(request):
    if request.method == 'POST':

        form = ImageCreationForm(data=request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            new_item.user = request.user
            new_item.save()
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
    return render(request, 'images/image/detail.html',
                  {'image': image,
                   'section': 'images'})

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
            else:
                image.user_like.remove(request.user)

            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    user = request.user

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(user)
            else:
                image.user_like.remove(user)
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