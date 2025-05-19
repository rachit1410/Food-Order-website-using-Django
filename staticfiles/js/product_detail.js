const mainImage = document.getElementById('main-product-image');
const thumbnailImages = document.querySelectorAll('.product-thumbnails img');
const colorOptions = document.querySelectorAll('.color-option');
const sizeOptions = document.querySelectorAll('.size-option');
const addToCartButton = document.querySelector('.add-to-cart');
const favoriteButton = document.querySelector('.add-to-favorites');
thumbnailImages.forEach(thumbnail => {
    thumbnail.addEventListener('click', () => {
        mainImage.src = thumbnail.dataset.image;
    });
});
colorOptions.forEach(color => {
    color.addEventListener('click', () => {
        colorOptions.forEach(c => c.classList.remove('active'));
        color.classList.add('active');
    });
});
sizeOptions.forEach(size => {
    size.addEventListener('click', () => {
        sizeOptions.forEach(s => s.classList.remove('active'));
        size.classList.add('active');
    });
});
addToCartButton.addEventListener('click', () => {
    alert('Added to cart!');
});
favoriteButton.addEventListener('click', () => {
    const heartIcon = favoriteButton.querySelector('i');
    if (heartIcon.classList.contains('far')) {
        heartIcon.classList.remove('far');
        heartIcon.classList.add('fas');
        alert('Added to favorites!');
    } else {
        heartIcon.classList.remove('fas');
        heartIcon.classList.add('far');
        alert('Removed from favorites!');
    }
});