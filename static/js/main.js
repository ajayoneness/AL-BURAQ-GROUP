/**
 * AL BURAQ GROUP - Main JavaScript
 * Interactive functionality and cart management
 */

// Cart functionality
const Cart = {
    async add(productId, quantity = 1) {
        try {
            const response = await fetch('/orders/cart/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken(),
                },
                body: JSON.stringify({ product_id: productId, quantity: quantity }),
            });

            const data = await response.json();

            if (data.success) {
                this.updateBadge(data.cart_count);
                this.showNotification(data.message, 'success');
            } else {
                this.showNotification(data.message, 'error');
            }

            return data;
        } catch (error) {
            console.error('Error adding to cart:', error);
            this.showNotification('Error adding to cart', 'error');
        }
    },

    async update(itemId, quantity) {
        try {
            const response = await fetch('/orders/cart/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken(),
                },
                body: JSON.stringify({ item_id: itemId, quantity: quantity }),
            });

            const data = await response.json();

            if (data.success) {
                this.updateBadge(data.cart_count);
                return data;
            }

            return data;
        } catch (error) {
            console.error('Error updating cart:', error);
        }
    },

    async remove(itemId) {
        try {
            const response = await fetch('/orders/cart/remove/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken(),
                },
                body: JSON.stringify({ item_id: itemId }),
            });

            const data = await response.json();

            if (data.success) {
                this.updateBadge(data.cart_count);
                this.showNotification(data.message, 'success');
            }

            return data;
        } catch (error) {
            console.error('Error removing from cart:', error);
        }
    },

    updateBadge(count) {
        const badge = document.getElementById('cartBadge');
        if (badge) {
            badge.textContent = count;
            badge.style.transform = 'scale(1.3)';
            setTimeout(() => {
                badge.style.transform = 'scale(1)';
            }, 200);
        }
    },

    getCsrfToken() {
        const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    },

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 9999;
            animation: slideIn 0.3s ease;
            min-width: 250px;
        `;
        notification.innerHTML = `
            ${message}
            <button onclick="this.parentElement.remove()" style="float: right; background: none; border: none; color: inherit; cursor: pointer; margin-left: 10px;">&times;</button>
        `;

        document.body.appendChild(notification);

        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
};

// Add to cart button handler
function addToCart(productId, quantity = 1) {
    Cart.add(productId, quantity);
}

// Quantity controls for product pages
function updateQuantity(input, delta) {
    const currentValue = parseInt(input.value) || 1;
    const minValue = parseInt(input.min) || 1;
    const newValue = Math.max(minValue, currentValue + delta);
    input.value = newValue;
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Image gallery for product pages
function initImageGallery() {
    const thumbs = document.querySelectorAll('.product-thumb');
    const mainImage = document.getElementById('mainProductImage');

    if (thumbs.length && mainImage) {
        thumbs.forEach(thumb => {
            thumb.addEventListener('click', function () {
                // Update main image
                mainImage.src = this.dataset.image;

                // Update active state
                thumbs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
}

// Search functionality
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    if (searchInput && searchResults) {
        let debounceTimer;

        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            const query = this.value.trim();

            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }

            debounceTimer = setTimeout(async () => {
                try {
                    const response = await fetch(`/store/search/?q=${encodeURIComponent(query)}&ajax=1`);
                    const data = await response.json();

                    if (data.products && data.products.length) {
                        searchResults.innerHTML = data.products.map(p => `
                            <a href="${p.url}" class="search-result-item">
                                <strong>${p.name}</strong>
                                <span>¥${p.price}</span>
                            </a>
                        `).join('');
                        searchResults.style.display = 'block';
                    } else {
                        searchResults.innerHTML = '<div class="search-no-results">No products found</div>';
                        searchResults.style.display = 'block';
                    }
                } catch (error) {
                    console.error('Search error:', error);
                }
            }, 300);
        });

        // Close search results when clicking outside
        document.addEventListener('click', function (e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
}

// Tracking page functionality
function initTracking() {
    const trackingForm = document.getElementById('trackingForm');
    const trackingInput = document.getElementById('trackingInput');
    const trackingResults = document.getElementById('trackingResults');

    if (trackingForm && trackingInput && trackingResults) {
        trackingForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const trackingNumber = trackingInput.value.trim();

            if (!trackingNumber) return;

            // Show loading
            trackingResults.innerHTML = '<div class="spinner" style="margin: 2rem auto;"></div>';
            trackingResults.style.display = 'block';

            try {
                const response = await fetch(`/tracking/ajax/?tracking=${encodeURIComponent(trackingNumber)}`);
                const data = await response.json();

                if (data.success) {
                    trackingResults.innerHTML = renderTrackingResult(data);
                } else {
                    trackingResults.innerHTML = `
                        <div class="alert alert-error">
                            <i class="fas fa-exclamation-circle"></i> ${data.error}
                        </div>
                    `;
                }
            } catch (error) {
                trackingResults.innerHTML = `
                    <div class="alert alert-error">
                        <i class="fas fa-exclamation-circle"></i> Error loading tracking information
                    </div>
                `;
            }
        });
    }
}

function renderTrackingResult(data) {
    const shipment = data.shipment;
    const updates = data.updates;

    return `
        <div class="card card-glass" style="padding: 2rem;">
            <div class="flex justify-between items-center mb-lg" style="flex-wrap: wrap; gap: 1rem;">
                <div>
                    <h3 style="color: var(--gold-light);">
                        <i class="fas fa-${shipment.shipping_method === 'air' ? 'plane' : shipment.shipping_method === 'sea' ? 'ship' : 'train'}"></i>
                        ${shipment.tracking_number}
                    </h3>
                    <p style="color: var(--text-secondary);">${shipment.shipping_method}</p>
                </div>
                <div class="badge badge-${shipment.progress >= 75 ? 'success' : 'gold'}">
                    ${shipment.current_status}
                </div>
            </div>
            
            <!-- Progress bar -->
            <div style="background: var(--bg-card); border-radius: 10px; height: 8px; margin-bottom: 2rem; overflow: hidden;">
                <div style="background: var(--gold-gradient); height: 100%; width: ${shipment.progress}%; transition: width 1s ease;"></div>
            </div>
            
            <!-- Route info -->
            <div class="flex justify-between mb-lg" style="flex-wrap: wrap; gap: 1rem;">
                <div>
                    <p style="color: var(--text-muted); font-size: 0.85rem;">From</p>
                    <p style="font-weight: 600;">${shipment.origin}</p>
                </div>
                <div style="text-align: center;">
                    <i class="fas fa-arrow-right" style="color: var(--gold-light);"></i>
                </div>
                <div style="text-align: right;">
                    <p style="color: var(--text-muted); font-size: 0.85rem;">To</p>
                    <p style="font-weight: 600;">${shipment.destination}</p>
                </div>
            </div>
            
            ${shipment.estimated_delivery ? `
            <div class="mb-lg">
                <p style="color: var(--text-muted); font-size: 0.85rem;">Estimated Delivery</p>
                <p style="font-weight: 600; color: var(--teal);">${shipment.estimated_delivery}</p>
            </div>
            ` : ''}
            
            <!-- Timeline -->
            <h4 class="mb-md">Tracking History</h4>
            <div class="tracking-timeline">
                ${updates.map((update, index) => `
                    <div class="timeline-item" style="display: flex; gap: 1rem; padding-bottom: 1rem; ${index < updates.length - 1 ? 'border-left: 2px solid var(--gold-primary); margin-left: 9px; padding-left: 1.5rem;' : ''}">
                        <div style="width: 20px; height: 20px; background: var(--gold-gradient); border-radius: 50%; flex-shrink: 0; ${index < updates.length - 1 ? 'margin-left: -2.1rem;' : ''}"></div>
                        <div>
                            <p style="font-weight: 600;">${update.status}</p>
                            <p style="color: var(--text-secondary); font-size: 0.9rem;">${update.description}</p>
                            <p style="color: var(--text-muted); font-size: 0.8rem;">${update.timestamp} - ${update.location}</p>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// FAQ Accordion
function initFaqAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');

        if (question && answer) {
            question.addEventListener('click', () => {
                const isOpen = item.classList.contains('active');

                // Close all other items
                faqItems.forEach(i => {
                    i.classList.remove('active');
                    i.querySelector('.faq-answer').style.maxHeight = null;
                });

                // Toggle current item
                if (!isOpen) {
                    item.classList.add('active');
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                }
            });
        }
    });
}

// Initialize all functionality
document.addEventListener('DOMContentLoaded', function () {
    initImageGallery();
    initSearch();
    initTracking();
    initFaqAccordion();

    // Add slideIn animation style
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
});

// Export for global use
window.Cart = Cart;
window.addToCart = addToCart;
window.updateQuantity = updateQuantity;
