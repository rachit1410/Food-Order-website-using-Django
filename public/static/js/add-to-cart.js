document.addEventListener('DOMContentLoaded', function() {
    // Plus/Minus quantity buttons
    document.querySelectorAll('.product-item').forEach(function(productItem) {
        const minusBtn = productItem.querySelector('.quantity-left-minus');
        const plusBtn = productItem.querySelector('.quantity-right-plus');
        const qtyInput = productItem.querySelector('input[name="quantity"]');

        if (minusBtn && qtyInput) {
            minusBtn.addEventListener('click', function(e) {
                e.preventDefault();
                let qty = parseInt(qtyInput.value) || 0;
                if (qty > 0) qtyInput.value = qty - 1;
            });
        }
        if (plusBtn && qtyInput) {
            plusBtn.addEventListener('click', function(e) {
                e.preventDefault();
                let qty = parseInt(qtyInput.value) || 0;
                qtyInput.value = qty + 1;
            });
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addToCart(itemId, quantity = 1) {
    console.log("function called with arguments: ",itemId, quantity);
    
    fetch('/api/add-to-cart/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({
            item_id: itemId,
            item_quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            alert('Added to cart!');
        } else {
            alert(data.message || 'Could not add to cart.');
        }
    })
    .catch(() => {
        alert('Could not add to cart. Please try again.');
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.product-item .addtocart-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            // Find the closest product-item and get the item id and quantity
            const productItem = btn.closest('.product-item');
            if (!productItem) return;
            const detailLink = productItem.querySelector('a[href*="item-detail"], a[href*="variant-detail"]');
            let itemId = null;
            if (detailLink) {
                const href = detailLink.getAttribute('href');
                if (href) {
                    // Remove trailing slash if present, then get last segment
                    const parts = href.replace(/\/$/, '').split('/');
                    itemId = parts[parts.length - 1];
                }
            }
            const qtyInput = productItem.querySelector('input[name="quantity"]');
            const quantity = qtyInput ? qtyInput.value : 1;

            if (itemId) {
                addToCart(itemId, quantity);
                qtyInput.value = 0
            }
        });
    });
});


