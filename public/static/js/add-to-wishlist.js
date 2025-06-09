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

function addToWishlist(itemId, wishlistButton) {
    console.log("function called with arguments: ",itemId);

    fetch('/api/add-to-wishlist/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({
            item_id: itemId,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (! data.status) {
            alert('Could not add to wishlist. Please try again.');
        }else{
            if (data.data.action) {
                wishlistButton.classList.remove('btn-wishlist');
                wishlistButton.classList.add('btn-wishlist-s');
            } else{
                wishlistButton.classList.remove('btn-wishlist-s');
                wishlistButton.classList.add('btn-wishlist');
            }
            wishlistButton.classList.add('btn-wishlist');
        }
    })
    .catch(() => {
        alert('Could not add to wishlist. Please try again.');
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.product-item .wishlist').forEach(btn => {

        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productItem = btn.closest('.product-item');
            if (!productItem) return;
            const detailLink = productItem.querySelector('a[href*="item-detail"], a[href*="variant-detail"]');
            let itemId = null;
            if (detailLink) {
                const href = detailLink.getAttribute('href');
                if (href) {
                    const parts = href.replace(/\/$/, '').split('/');
                    itemId = parts[parts.length - 1];
                }
            }
            wishlistButton = btn.closest('.wishlist')
            if (itemId) {
                addToWishlist(itemId, wishlistButton);
            }
        });
    });
});