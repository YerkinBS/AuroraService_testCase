from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import DocumentForm
from django.http import HttpResponseRedirect
from .models import Document
from django.shortcuts import get_object_or_404


@login_required
def profile_view(request):
    files = request.user.document_set.all()
    return render(request, 'web/profile.html', {'files': files})


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.save()
        return redirect('login')
    

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return HttpResponseRedirect('/profile/')
    else:
        form = DocumentForm
    return render(request, 'web/upload.html', {'form': form})


def delete_document(request, pk):
    file = request.user.document_set.get(pk=pk)
    file.delete()
    return redirect('profile')


@login_required
def update_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id, author=request.user)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile/')
    else:
        form = DocumentForm(instance=document)

    return render(request, 'web/update.html', {'form': form})