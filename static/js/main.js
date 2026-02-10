/**
 * AL BURAQ GROUP - Main JavaScript
 * Interactive functionality and cart management
 */

// doing some changes for server tessting

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

    // Trigger animation shortly after rendering
    setTimeout(() => {
        const progressBar = document.querySelector('.progress-bar-fill');
        if (progressBar) {
            progressBar.style.width = `${shipment.progress}%`;
        }
    }, 100);

    return `
        <div class="card card-glass" style="padding: 0; overflow: hidden; border: 1px solid rgba(212, 175, 55, 0.2); background: rgba(18, 18, 24, 0.8);" data-aos="fade-up">
            
            <!-- Status Header -->
            <div style="padding: 2rem; border-bottom: 1px solid rgba(255,255,255,0.05); background: linear-gradient(90deg, rgba(212, 175, 55, 0.05), transparent);">
                <div class="flex justify-between items-start mb-lg" style="flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <div class="flex items-center gap-sm mb-xs">
                            <span style="background: var(--gold-primary); color: #000; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 700;">${shipment.shipping_method.toUpperCase()}</span>
                            <span style="color: var(--text-muted); font-size: 0.9rem;">#${shipment.tracking_number}</span>
                        </div>
                        <h2 style="font-size: 1.8rem; margin: 0; color: #fff;">${shipment.current_status}</h2>
                        <p style="color: var(--text-secondary); margin-top: 0.25rem;">Updated: ${new Date().toISOString().slice(0, 16).replace('T', ' ')}</p>
                    </div>
                    <div style="text-align: right;">
                         <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, var(--gold-primary), var(--gold-dark)); color: #000; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; box-shadow: 0 10px 20px rgba(212, 175, 55, 0.3);">
                            ${shipment.shipping_method.toLowerCase().includes('air') ? '<i class="fas fa-plane"></i>' : 
                              shipment.shipping_method.toLowerCase().includes('sea') ? '<i class="fas fa-ship"></i>' : 
                              '<i class="fas fa-train"></i>'}
                        </div>
                    </div>
                </div>

                <!-- Progress Bar -->
                <div style="margin-top: 2rem;">
                     <div class="flex justify-between mb-xs" style="font-size: 0.85rem; font-weight: 600; color: var(--text-secondary);">
                        <span>Progress</span>
                        <span>${shipment.progress}%</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px; overflow: hidden; position: relative;">
                        <div class="progress-bar-fill" style="background: var(--gold-gradient); height: 100%; width: 0%; border-radius: 10px; transition: width 1.5s cubic-bezier(0.22, 1, 0.36, 1); box-shadow: 0 0 15px rgba(212, 175, 55, 0.5);"></div>
                    </div>
                </div>
            </div>

            <!-- Route & Details -->
            <div class="grid grid-cols-3 gap-0" style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                 <div style="padding: 2rem; border-right: 1px solid rgba(255,255,255,0.05);">
                    <p style="color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">Origin</p>
                    <div class="flex items-center gap-sm">
                        <i class="fas fa-map-marker-alt" style="color: var(--gold-light);"></i>
                        <span style="font-weight: 600; font-size: 1.1rem;">${shipment.origin}</span>
                    </div>
                 </div>
                 <div style="padding: 2rem; border-right: 1px solid rgba(255,255,255,0.05); text-align: center; display: flex; flex-direction: column; justify-content: center;">
                    <i class="fas fa-arrow-right" style="color: var(--text-muted); font-size: 1.5rem; opacity: 0.5;"></i>
                 </div>
                 <div style="padding: 2rem;">
                    <p style="color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">Destination</p>
                    <div class="flex items-center gap-sm">
                        <i class="fas fa-map-marker-alt" style="color: var(--teal);"></i>
                        <span style="font-weight: 600; font-size: 1.1rem;">${shipment.destination}</span>
                    </div>
                 </div>
            </div>

            <!-- Info Grid -->
            <div class="grid grid-cols-3 gap-0" style="background: rgba(0,0,0,0.2);">
                ${shipment.estimated_delivery ? `
                <div style="padding: 1.5rem; text-align: center; border-right: 1px solid rgba(255,255,255,0.05);">
                    <i class="fas fa-calendar-alt mb-xs" style="color: var(--gold-light); font-size: 1.2rem;"></i>
                    <p style="color: var(--text-muted); font-size: 0.8rem; margin-bottom: 0.2rem;">Est. Delivery</p>
                    <p style="font-weight: 600; color: #fff;">${shipment.estimated_delivery}</p>
                </div>
                ` : ''}
                <div style="padding: 1.5rem; text-align: center; border-right: 1px solid rgba(255,255,255,0.05);">
                    <i class="fas fa-box mb-xs" style="color: var(--gold-light); font-size: 1.2rem;"></i>
                     <p style="color: var(--text-muted); font-size: 0.8rem; margin-bottom: 0.2rem;">Packages</p>
                    <p style="font-weight: 600; color: #fff;">${shipment.total_packages}</p>
                </div>
                ${shipment.total_weight ? `
                <div style="padding: 1.5rem; text-align: center;">
                    <i class="fas fa-weight-hanging mb-xs" style="color: var(--gold-light); font-size: 1.2rem;"></i>
                    <p style="color: var(--text-muted); font-size: 0.8rem; margin-bottom: 0.2rem;">Weight</p>
                    <p style="font-weight: 600; color: #fff;">${shipment.total_weight} kg</p>
                </div>
                ` : ''}
            </div>

            <!-- Timeline -->
            <div style="padding: 2rem;">
                <h4 class="mb-lg" style="color: var(--gold-primary);">Tracking History</h4>
                <div class="tracking-timeline">
                    ${updates.map((update, index) => `
                        <div class="timeline-item" style="display: flex; gap: 1.5rem; position: relative; padding-bottom: 2rem; opacity: 0; animation: fadeSlideIn 0.5s ease forwards; animation-delay: ${(index + 2) * 100}ms;">
                            ${index < updates.length - 1 ? 
                            '<div style="position: absolute; left: 19px; top: 40px; bottom: 0; width: 2px; background: rgba(255,255,255,0.1);"></div>' : ''}
                            
                            <div style="width: 40px; height: 40px; background: ${index === 0 ? 'var(--gold-gradient)' : 'rgba(255,255,255,0.1)'}; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; z-index: 1;">
                                <i class="fas fa-check" style="font-size: 0.9rem; color: ${index === 0 ? '#000' : 'var(--text-muted)'};"></i>
                            </div>
                            
                            <div style="padding-top: 0.2rem;">
                                <p style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.3rem; color: ${index === 0 ? '#fff' : 'var(--text-secondary)'};">${update.status}</p>
                                <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 0.3rem; line-height: 1.5;">${update.description}</p>
                                <p style="color: var(--text-muted); font-size: 0.85rem; display: flex; align-items: center; gap: 0.5rem;">
                                    <i class="far fa-clock"></i> ${update.timestamp}
                                    ${update.location ? `<span>•</span> <i class="fas fa-map-pin"></i> ${update.location}` : ''}
                                </p>
                            </div>
                        </div>
                    `).join('')}
                    ${updates.length === 0 ? 
                    '<p style="color: var(--text-muted); text-align: center; padding: 2rem;">No tracking updates available yet.</p>' : ''}
                </div>
            </div>
            
            <style>
                @keyframes fadeSlideIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            </style>
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
