from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ImageCreationForm

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