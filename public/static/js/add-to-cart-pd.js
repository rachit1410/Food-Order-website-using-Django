
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
    document.querySelector('#addToCartButton').addEventListener('click', function(e) {
        e.preventDefault();
        // Find the closest product-item and get the item id and quantity
        const currentUrl = window.location.href;
        const urlParts = currentUrl.split('/');
        const itemId = urlParts[urlParts.length - 2] || urlParts[urlParts.length - 1];
        const quantity = 1;

        if (itemId) {
            addToCart(itemId, quantity);
        }
    });
});
