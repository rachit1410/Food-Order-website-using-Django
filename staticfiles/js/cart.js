const cartItemsElement = document.getElementById('cart-items');
        const totalPriceElement = document.getElementById('total-price');
        const checkoutMessage = document.getElementById('checkout-message');

        // Sample cart data (replace with actual data from localStorage or an API)
        let cart = [
            { id: 1, name: 'Product 1', price: 19.99, quantity: 2, image: 'https://via.placeholder.com/150' },
            { id: 2, name: 'Product 2', price: 29.99, quantity: 1, image: 'https://via.placeholder.com/150' },
            { id: 3, name: 'Product 3', price: 15.50, quantity: 3, image: 'https://via.placeholder.com/150' },
        ];

        function updateCart() {
            cartItemsElement.innerHTML = '';
            let totalPrice = 0;

            if (cart.length === 0) {
                cartItemsElement.innerHTML = '<p class="text-gray-500 text-center py-4">Your cart is empty.</p>';
                totalPriceElement.textContent = '0.00';
                return;
            }

            cart.forEach(item => {
                const itemElement = document.createElement('div');
                itemElement.classList.add('flex', 'items-center', 'justify-between', 'border-bottom', 'border-light-blue', 'py-4');

                const itemDetails = document.createElement('div');
                itemDetails.classList.add('flex', 'items-center');

                const itemImage = document.createElement('img');
                itemImage.src = item.image;
                itemImage.alt = item.name;
                itemImage.classList.add('w-20', 'h-20', 'rounded-md', 'mr-4');

                const itemNamePrice = document.createElement('div');
                itemNamePrice.classList.add('flex', 'flex-col');
                const itemName = document.createElement('span');
                itemName.textContent = item.name;
                itemName.classList.add('text-lg', 'font-semibold', 'text-gray-900');
                const itemPrice = document.createElement('span');
                itemPrice.textContent = `$${item.price.toFixed(2)}`;
                itemPrice.classList.add('text-gray-700');
                itemNamePrice.appendChild(itemName);
                itemNamePrice.appendChild(itemPrice);

                itemDetails.appendChild(itemImage);
                itemDetails.appendChild(itemNamePrice);

                const itemQuantity = document.createElement('div');
                itemQuantity.classList.add('flex', 'items-center');

                const decreaseButton = document.createElement('button');
                decreaseButton.textContent = '-';
                decreaseButton.classList.add('quantity-button', 'text-light-blue', 'hover:text-blue-400', 'border-light-blue');
                decreaseButton.onclick = () => {
                    if (item.quantity > 1) {
                        item.quantity--;
                        updateCart();
                    }
                };

                const quantityInput = document.createElement('input');
                quantityInput.type = 'number';
                quantityInput.value = item.quantity;
                quantityInput.classList.add('quantity-input');
                quantityInput.min = '1';
                quantityInput.onchange = (event) => {
                    const newQuantity = parseInt(event.target.value);
                    if (!isNaN(newQuantity) && newQuantity > 0) {
                        item.quantity = newQuantity;
                        updateCart();
                    }
                };

                const increaseButton = document.createElement('button');
                increaseButton.textContent = '+';
                increaseButton.classList.add('quantity-button', 'text-light-blue', 'hover:text-blue-400', 'border-light-blue');
                increaseButton.onclick = () => {
                    item.quantity++;
                    updateCart();
                };

                const itemTotal = document.createElement('span');
                itemTotal.textContent = `$${(item.price * item.quantity).toFixed(2)}`;
                itemTotal.classList.add('text-lg', 'font-semibold', 'text-gray-900', 'ml-6');

                itemQuantity.appendChild(decreaseButton);
                itemQuantity.appendChild(quantityInput);
                itemQuantity.appendChild(increaseButton);
                itemQuantity.appendChild(itemTotal);

                itemElement.appendChild(itemDetails);
                itemElement.appendChild(itemQuantity);
                cartItemsElement.appendChild(itemElement);

                totalPrice += item.price * item.quantity;
            });

            totalPriceElement.textContent = totalPrice.toFixed(2);
        }

        function checkout() {
            // In a real application, you would send the cart data to a server for processing
            console.log('Checkout:', cart);
            checkoutMessage.classList.remove('hidden');
            // Clear the cart (in a real app, you might want to keep a record of the order)
            // cart = [];  <-- REMOVED THIS LINE
            updateCart();
             setTimeout(() => {
                checkoutMessage.classList.add('hidden');
             }, 3000);
        }

        // Initial render of the cart
        updateCart();