// DOM Elements
const collectionTitleInput = document.getElementById('collectionTitle');
const collectionDescriptionInput = document.getElementById('collectionDescription');
const coverImageInput = document.getElementById('coverImageInput');
const coverImagePreview = document.getElementById('coverImagePreview');
const imagePreviewContainer = document.getElementById('imagePreviewContainer');
const productSearchInput = document.getElementById('productSearch');
const availableProductsList = document.getElementById('availableProductsList');
const selectedProductsList = document.getElementById('selectedProductsList');
const saveCollectionButton = document.getElementById('saveCollectionButton');
const goToHomeButton = document.getElementById('goToHomeButton');
const saveMessage = document.getElementById('saveMessage');

// This will hold the products fetched from Django
let allProducts = [];
let availableProducts = [];
let selectedProductIds = new Set();

// --- Data Fetching from Django ---
async function fetchProductsFromDjango(searchTerm = "") {
    try {
        const url = `/api/search-products/?q=${encodeURIComponent(searchTerm)}`;
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.status && data.data.items) {
            allProducts = data.data.items;
            availableProducts = [...allProducts];
            renderAvailableProducts();
        } else {
            availableProducts = [];
            renderAvailableProducts();
            availableProductsList.innerHTML = `<p class="text-red-600 text-center py-4">${data.message || "Failed to load products."}</p>`;
        }
    } catch (error) {
        console.error('Error fetching products:', error);
        availableProductsList.innerHTML = '<p class="text-red-600 text-center py-4">Failed to load products. Please try again.</p>';
    }
}

// --- Frontend Rendering Functions ---

function renderAvailableProducts() {
    availableProductsList.innerHTML = '';
    if (availableProducts.length === 0) {
        availableProductsList.innerHTML = '<p class="text-gray-500 text-center py-4">No products found.</p>';
        return;
    }

    availableProducts.forEach(product => {
        const isSelected = selectedProductIds.has(product.id);
        const productItem = document.createElement('div');
        productItem.className = `flex items-center justify-between p-2 rounded-md ${isSelected ? 'bg-indigo-100' : 'bg-gray-50'} border border-gray-200`;
        productItem.innerHTML = `
            <label class="flex items-center cursor-pointer flex-grow">
                <input type="checkbox" data-product-id="${product.id}" class="form-checkbox h-4 w-4 text-green-600 rounded" ${isSelected ? 'checked' : ''}>
                <span class="ml-2 text-gray-800 font-medium">${product.item_name}</span>
            </label>
            <span class="text-sm text-gray-600">₹${product.item_price}</span>
        `;
        availableProductsList.appendChild(productItem);
    });
    addCheckboxListeners();
}

function renderSelectedProducts() {
    selectedProductsList.innerHTML = '';
    if (selectedProductIds.size === 0) {
        selectedProductsList.innerHTML = '<p class="text-gray-500 text-center py-4">No products selected.</p>';
        return;
    }

    const selectedProducts = allProducts.filter(p => selectedProductIds.has(p.id));
    selectedProducts.forEach(product => {
        const productItem = document.createElement('div');
        productItem.className = `flex items-center justify-between p-2 rounded-md bg-green-100 border border-green-200`;
        productItem.innerHTML = `
            <span class="text-gray-800 font-medium">${product.item_name}</span>
            <button data-product-id="${product.id}" class="remove-product-btn text-red-600 hover:text-red-800 text-sm font-semibold ml-4">Remove</button>
        `;
        selectedProductsList.appendChild(productItem);
    });
    addRemoveButtonListeners();
}

// --- Event Listeners ---

function addCheckboxListeners() {
    document.querySelectorAll('#availableProductsList input[type="checkbox"]').forEach(checkbox => {
        checkbox.onchange = (event) => {
            const productId = event.target.getAttribute('data-product-id');
            if (event.target.checked) {
                selectedProductIds.add(productId);
            } else {
                selectedProductIds.delete(productId);
            }
            renderAvailableProducts();
            renderSelectedProducts();
        };
    });
}

function addRemoveButtonListeners() {
    document.querySelectorAll('.remove-product-btn').forEach(button => {
        button.onclick = (event) => {
            const productId = event.target.dataset.productId;
            selectedProductIds.delete(productId);
            renderAvailableProducts();
            renderSelectedProducts();
        };
    });
}

// Product search input event
productSearchInput.addEventListener('input', (event) => {
    const searchTerm = event.target.value.trim();
    fetchProductsFromDjango(searchTerm);
});

// Cover image preview
coverImageInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            coverImagePreview.src = e.target.result;
            imagePreviewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    } else {
        imagePreviewContainer.classList.add('hidden');
        coverImagePreview.src = '#';
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Save Collection button
saveCollectionButton.addEventListener('click', async () => {
    const title = collectionTitleInput.value.trim();
    const description = collectionDescriptionInput.value.trim();
    const coverImageFile = coverImageInput.files[0];
    const selectedProductIdsArray = Array.from(selectedProductIds);

    if (!title) {
        saveMessage.textContent = 'Please enter a collection title.';
        saveMessage.classList.remove('hidden', 'text-green-700');
        saveMessage.classList.add('text-red-700');
        return;
    }
    if (selectedProductIdsArray.length === 0) {
        saveMessage.textContent = 'Please select at least one product for the collection.';
        saveMessage.classList.remove('hidden', 'text-green-700');
        saveMessage.classList.add('text-red-700');
        return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('products', JSON.stringify(selectedProductIdsArray));
    if (coverImageFile) {
        formData.append('cover_image', coverImageFile);
    }

    try {
        const response = await fetch('/create-collection/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        saveMessage.textContent = 'Collection saved successfully!';
        saveMessage.classList.remove('hidden', 'text-red-700');
        saveMessage.classList.add('text-green-700');

        // Clear form after successful save
        collectionTitleInput.value = '';
        collectionDescriptionInput.value = '';
        coverImageInput.value = '';
        coverImagePreview.src = '#';
        imagePreviewContainer.classList.add('hidden');
        selectedProductIds.clear();
        availableProducts = [...allProducts];
        renderAvailableProducts();
        renderSelectedProducts();

        saveCollectionButton.classList.add('hidden');
        goToHomeButton.classList.remove('hidden');

    } catch (error) {
        console.error('Error saving collection:', error);
        saveMessage.textContent = `Failed to save collection: ${error.message}`;
        saveMessage.classList.remove('hidden', 'text-green-700');
        saveMessage.classList.add('text-red-700');
        saveCollectionButton.classList.remove('hidden');
        goToHomeButton.classList.add('hidden');
    } finally {
        setTimeout(() => {
            saveMessage.classList.add('hidden');
        }, 3000);
    }
});

// Go to Home button
goToHomeButton.addEventListener('click', () => {
    window.location.href = '/'; // Redirect to your Django home URL
});

// Initial rendering
fetchProductsFromDjango();
renderSelectedProducts();