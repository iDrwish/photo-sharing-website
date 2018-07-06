from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    return render(request, 'images/image/details.html',
                  {'image': image,
                   'section': 'images'})
