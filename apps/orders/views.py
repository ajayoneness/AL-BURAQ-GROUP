from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext as _
import json
import urllib.parse

from .models import Cart, CartItem, Order, OrderItem
from apps.store.models import Product
from .utils import generate_order_excel


def get_or_create_cart(request):
    """Get or create cart based on user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_view(request):
    """View cart contents"""
    cart = get_or_create_cart(request)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product__category').all(),
    }
    return render(request, 'orders/cart.html', context)


@require_POST
def add_to_cart(request):
    """Add product to cart (AJAX)"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        cart = get_or_create_cart(request)
        
        # Check if product already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': _('Product added to cart'),
            'cart_count': cart.get_items_count(),
            'cart_total': float(cart.get_total()),
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@require_POST
def update_cart_item(request):
    """Update cart item quantity (AJAX)"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_items_count(),
            'cart_total': float(cart.get_total()),
            'item_total': float(cart_item.get_total()) if quantity > 0 else 0,
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@require_POST
def remove_from_cart(request):
    """Remove item from cart (AJAX)"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': _('Item removed from cart'),
            'cart_count': cart.get_items_count(),
            'cart_total': float(cart.get_total()),
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    
    if cart.get_items_count() == 0:
        messages.warning(request, _('Your cart is empty'))
        return redirect('store:category_list')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key or '',
            customer_name=request.POST.get('customer_name', ''),
            customer_email=request.POST.get('customer_email', ''),
            customer_phone=request.POST.get('customer_phone', ''),
            customer_company=request.POST.get('customer_company', ''),
            customer_country=request.POST.get('customer_country', ''),
            notes=request.POST.get('notes', ''),
        )
        
        # Create order items from cart
        for cart_item in cart.items.select_related('product__category').all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.safe_translation_getter('name', any_language=True) or '',
                category_name=cart_item.product.category.safe_translation_getter('name', any_language=True) or '',
                quantity=cart_item.quantity,
                unit=cart_item.product.unit,
                unit_price=cart_item.product.price_rmb,
            )
        
        # Calculate totals
        order.calculate_totals()
        
        # Generate Excel file
        excel_file = generate_order_excel(order)
        order.excel_file = excel_file
        order.status = 'sent_to_whatsapp'
        order.save()
        
        # Clear cart
        cart.clear()
        
        # Redirect to WhatsApp confirmation page
        return redirect('orders:order_complete', order_number=order.order_number)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product__category').all(),
    }
    return render(request, 'orders/checkout.html', context)


def order_complete(request, order_number):
    """Order complete page with WhatsApp redirect"""
    order = get_object_or_404(Order, order_number=order_number)
    
    # Generate WhatsApp message
    whatsapp_message = f"""🛒 *New Order from AL BURAQ Website*

📦 *Order Number:* {order.order_number}
👤 *Customer:* {order.customer_name}
📱 *Phone:* {order.customer_phone}
📧 *Email:* {order.customer_email or 'N/A'}
🏢 *Company:* {order.customer_company or 'N/A'}
🌍 *Country:* {order.customer_country or 'N/A'}

🛍️ *Order Summary:*
• Total Items: {order.total_items}
• Subtotal: ¥{order.subtotal} RMB

📋 *Items:*
"""
    for item in order.items.all():
        whatsapp_message += f"• {item.product_name} x{item.quantity} ({item.unit}) = ¥{item.get_total()}\n"
    
    if order.notes:
        whatsapp_message += f"\n📝 *Notes:* {order.notes}"
    
    whatsapp_message += "\n\n_Please find the detailed Excel file attached._"
    
    # URL encode the message
    encoded_message = urllib.parse.quote(whatsapp_message)
    whatsapp_url = f"https://wa.me/{settings.COMPANY_WHATSAPP.replace('+', '')}?text={encoded_message}"
    
    context = {
        'order': order,
        'whatsapp_url': whatsapp_url,
    }
    return render(request, 'orders/order_complete.html', context)


def download_order_excel(request, order_number):
    """Download order Excel file"""
    order = get_object_or_404(Order, order_number=order_number)
    
    if not order.excel_file:
        # Generate Excel if not exists
        excel_file = generate_order_excel(order)
        order.excel_file = excel_file
        order.save()
    
    return FileResponse(
        order.excel_file.open('rb'),
        as_attachment=True,
        filename=f"AL_BURAQ_Order_{order.order_number}.xlsx"
    )


def cart_count(request):
    """Get cart count (AJAX)"""
    cart = get_or_create_cart(request)
    return JsonResponse({
        'count': cart.get_items_count(),
        'total': float(cart.get_total()),
    })
