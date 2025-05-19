        const productList = document.getElementById('product-list');
        const noResultsMessage = document.getElementById('no-results');

        // Sample product data (replace with your actual data source)
        const products = [
            { id: 1, name: 'Laptop', category: 'electronics', price: 800, image: 'https://via.placeholder.com/150' },
            { id: 2, name: 'T-Shirt', category: 'clothing', price: 25, image: 'https://via.placeholder.com/150' },
            { id: 3, name: 'Garden Chair', category: 'home-garden', price: 75, image: 'https://via.placeholder.com/150' },
            { id: 4, name: 'Book: The Art of Programming', category: 'books', price: 30, image: 'https://via.placeholder.com/150' },
            { id: 5, name: 'Smartphone', category: 'electronics', price: 600, image: 'https://via.placeholder.com/150' },
            { id: 6, name: 'Jeans', category: 'clothing', price: 50, image: 'https://via.placeholder.com/150' },
            { id: 7, name: 'Coffee Table', category: 'home-garden', price: 120, image: 'https://via.placeholder.com/150' },
            { id: 8, name: 'Book: Data Science Handbook', category: 'books', price: 40, image: 'https://via.placeholder.com/150' },
            { id: 9, name: 'Gaming Mouse', category: 'electronics', price: 50, image: 'https://via.placeholder.com/150' },
            { id: 10, name: 'Hoodie', category: 'clothing', price: 40, image: 'https://via.placeholder.com/150' },
            { id: 11, name: 'Outdoor Sofa', category: 'home-garden', price: 250, image: 'https://via.placeholder.com/150' },
            { id: 12, name: 'Book: Machine Learning Basics', category: 'books', price: 35, image: 'https://via.placeholder.com/150' },
        ];

        function displayProducts(filteredProducts) {
            productList.innerHTML = '';
            if (filteredProducts.length === 0) {
                noResultsMessage.classList.remove('hidden');
            } else {
                noResultsMessage.classList.add('hidden');
                filteredProducts.forEach(product => {
                    const productCard = document.createElement('div');
                    productCard.classList.add('bg-white', 'shadow-md', 'rounded-lg', 'p-4', 'flex', 'flex-col', 'transition-transform', 'hover:scale-105');

                    const productImage = document.createElement('img');
                    productImage.src = product.image;
                    productImage.alt = product.name;
                    productImage.classList.add('w-full', 'h-40', 'object-cover', 'rounded-md', 'mb-4');

                    const productName = document.createElement('h3');
                    productName.textContent = product.name;
                    productName.classList.add('text-lg', 'font-semibold', 'text-gray-900', 'mb-2');

                    const productCategory = document.createElement('span');
                    productCategory.textContent = `Category: ${product.category}`;
                    productCategory.classList.add('text-gray-600', 'text-sm', 'mb-1');

                    const productPrice = document.createElement('p');
                    productPrice.textContent = `$${product.price.toFixed(2)}`;
                    productPrice.classList.add('text-xl', 'font-bold', 'text-blue-600');

                    productCard.appendChild(productImage);
                    productCard.appendChild(productName);
                    productCard.appendChild(productCategory);
                    productCard.appendChild(productPrice);
                    productList.appendChild(productCard);
                });
            }
        }

        function applyFilters() {
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const categories = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                .map(checkbox => checkbox.value);
            const minPrice = parseFloat(document.getElementById('min-price').value) || 0;
            const maxPrice = parseFloat(document.getElementById('max-price').value) || Infinity;
            const sortValue = document.getElementById('sort').value;

            let filteredProducts = products.filter(product => {
                const searchMatch = product.name.toLowerCase().includes(searchTerm);
                const categoryMatch = categories.length === 0 || categories.includes(product.category);
                const priceMatch = product.price >= minPrice && product.price <= maxPrice;
                return searchMatch && categoryMatch && priceMatch;
            });

            switch (sortValue) {
                case 'price-asc':
                    filteredProducts.sort((a, b) => a.price - b.price);
                    break;
                case 'price-desc':
                    filteredProducts.sort((a, b) => b.price - a.price);
                    break;
                case 'name-asc':
                    filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
                    break;
                case 'name-desc':
                    filteredProducts.sort((a, b) => b.name.localeCompare(a.name));
                    break;
                default:
                    // No sorting (relevance)
                    break;
            }

            displayProducts(filteredProducts);
        }

        // Initial display of all products
        displayProducts(products);