from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from properties.models import SavedProperty


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next', 'core:home'))
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:home')


@login_required
def dashboard(request):
    saved = SavedProperty.objects.filter(user=request.user).select_related('property').prefetch_related('property__images')[:6]
    return render(request, 'accounts/dashboard.html', {
        'saved_properties': saved,
        'page_title': 'My Dashboard',
    })
