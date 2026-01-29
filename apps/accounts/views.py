from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from apps.orders.models import Order, Cart


def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Registration successful! Welcome to AL BURAQ GROUP.'))
            return redirect('accounts:dashboard')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def user_login(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Transfer session cart to user
            session_key = request.session.session_key
            if session_key:
                try:
                    session_cart = Cart.objects.get(session_key=session_key)
                    user_cart, created = Cart.objects.get_or_create(user=user)
                    
                    # Transfer items
                    for item in session_cart.items.all():
                        item.cart = user_cart
                        item.save()
                    
                    session_cart.delete()
                except Cart.DoesNotExist:
                    pass
            
            login(request, user)
            messages.success(request, _('Welcome back!'))
            
            next_url = request.GET.get('next', 'accounts:dashboard')
            return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def user_logout(request):
    """User logout"""
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect('core:home')


@login_required
def dashboard(request):
    """User dashboard"""
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')[:10]
    
    context = {
        'user': user,
        'orders': orders,
        'total_orders': Order.objects.filter(user=user).count(),
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    """User profile edit"""
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile,
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully!'))
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.profile, user=request.user)
    
    context = {'form': form}
    return render(request, 'accounts/profile.html', context)


@login_required
def order_history(request):
    """User order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/order_history.html', context)


@login_required
def order_detail(request, order_number):
    """User order detail"""
    from django.shortcuts import get_object_or_404
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'accounts/order_detail.html', context)
