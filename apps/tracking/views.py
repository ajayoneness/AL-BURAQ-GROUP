from django.shortcuts import render
from django.http import JsonResponse
from .models import Shipment


from apps.orders.models import Order

class VirtualUpdate:
    """Wrapper for virtual updates"""
    def __init__(self, order):
        self.location = 'System'
        self.description = f"Order #{order.order_number} has been placed."
        self.timestamp = order.created_at
        self._status_display = 'Order Placed'
    
    def get_status_display(self):
        return self._status_display

class VirtualShipment:
    """Wrapper to display Order as a Shipment"""
    def __init__(self, order):
        self.order = order
        self.tracking_number = order.order_number
        self.customer_name = order.customer_name
        self.origin = 'China'
        self.destination = order.customer_country or "Pending"
        self.shipping_method = 'standard'
        self.total_packages = order.total_items
        self.total_weight = 0
        self.estimated_delivery = None
        
        # Map status
        self.status_map = {
            'pending': ('order_received', 10),
            'sent_to_whatsapp': ('order_received', 15),
            'confirmed': ('sourcing', 30),
            'processing': ('quality_check', 50),
            'completed': ('delivered', 100),
            'cancelled': ('cancelled', 0),
        }
        self.current_status, self.percentage = self.status_map.get(order.status, ('order_received', 10))
        
    def get_shipping_method_display(self):
        return "Standard Shipping"
        
    def get_current_status_display(self):
        return self.current_status.replace('_', ' ').title()
        
    def get_status_percentage(self):
        return self.percentage
         
    @property
    def updates(self):
        return self
         
    def all(self):
        return [VirtualUpdate(self.order)]

def tracking_page(request):
    """Main tracking page"""
    tracking_number = request.GET.get('tracking', '')
    shipment = None
    error = None
    
    if tracking_number:
        try:
            shipment = Shipment.objects.prefetch_related('updates').get(
                tracking_number__iexact=tracking_number.strip()
            )
        except Shipment.DoesNotExist:
            # Try searching for Order
            try:
                order = Order.objects.get(order_number__iexact=tracking_number.strip())
                shipment = VirtualShipment(order)
            except Order.DoesNotExist:
                error = "No shipment or order found with this tracking number."
    
    context = {
        'tracking_number': tracking_number,
        'shipment': shipment,
        'error': error,
    }
    return render(request, 'tracking/tracking.html', context)


def track_ajax(request):
    """AJAX tracking lookup"""
    tracking_number = request.GET.get('tracking', '')
    
    if not tracking_number:
        return JsonResponse({
            'success': False,
            'error': 'Please enter a tracking number.'
        })
    
    shipment = None
    try:
        shipment = Shipment.objects.prefetch_related('updates').get(
            tracking_number__iexact=tracking_number.strip()
        )
    except Shipment.DoesNotExist:
        try:
            order = Order.objects.get(order_number__iexact=tracking_number.strip())
            shipment = VirtualShipment(order)
        except Order.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'No shipment or order found with this tracking number.'
            })
            
    # Process shipment (real or virtual)
    updates = []
    for update in shipment.updates.all():
        updates.append({
            'status': update.get_status_display(),
            'location': update.location,
            'description': update.description,
            'timestamp': update.timestamp.strftime('%Y-%m-%d %H:%M'),
        })
    
    return JsonResponse({
        'success': True,
        'shipment': {
            'tracking_number': shipment.tracking_number,
            'customer_name': shipment.customer_name,
            'current_status': shipment.get_current_status_display(),
            'shipping_method': shipment.get_shipping_method_display(),
            'origin': shipment.origin,
            'destination': shipment.destination,
            'estimated_delivery': shipment.estimated_delivery.strftime('%Y-%m-%d') if shipment.estimated_delivery else None,
            'progress': shipment.get_status_percentage(),
            'total_packages': shipment.total_packages,
            'total_weight': float(shipment.total_weight) if shipment.total_weight else None,
        },
        'updates': updates,
    })
