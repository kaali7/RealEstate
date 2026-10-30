from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from contacts.models import Contact


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')
    password2 = request.POST.get('password2', '')

    if password != password2:
        messages.error(request, 'Passwords do not match')
        return redirect('register')

    if User.objects.filter(username=username).exists():
        messages.error(request, 'The username is taken')
        return redirect('register')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'The email is being used')
        return redirect('register')

    User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    messages.success(request, 'You are now registered and can log in')
    return redirect('login')


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        messages.success(request, 'You are now logged in')
        return redirect('dashboard')

    messages.error(request, 'Invalid credentials')
    return redirect('login')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged Out')
    return redirect('index')


@login_required(login_url='login')
def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(
        user_id=request.user.id
    )
    context = {
        'contacts': user_contacts,
    }
    return render(request, 'accounts/dashboard.html', context)
