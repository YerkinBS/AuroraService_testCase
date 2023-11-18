from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy


@login_required
def profile_view(request):
    return render(request, 'web/profile.html')


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.save()
        return redirect('login')