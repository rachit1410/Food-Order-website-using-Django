const orderSummaryElement = document.getElementById('order-summary');
        const orderTotalElement = document.getElementById('order-total');
        const paymentIdElement = document.getElementById('payment-id'); // Get the payment ID element

        // Sample cart data (replace with actual data from localStorage or an API)
        let cart = [
            { id: 1, name: 'Product 1', price: 19.99, quantity: 2, image: 'https://via.placeholder.com/100' },
            { id: 2, name: 'Product 2', price: 29.99, quantity: 1, image: 'https://via.placeholder.com/100' },
            { id: 3, name: 'Product 3', price: 15.50, quantity: 3, image: 'https://via.placeholder.com/100' },
        ];

        // Simulate a payment ID (in a real app, this would come from your payment gateway)
        const simulatedPaymentId = "txn_" + Math.random().toString(36).substring(7);

        function displayOrderSummary() {
            orderSummaryElement.innerHTML = '';
            let orderTotal = 0;

            cart.forEach(item => {
                const itemElement = document.createElement('div');
                itemElement.classList.add('flex', 'items-center', 'justify-between', 'border-bottom', 'border-light-blue', 'py-2');

                const itemDetails = document.createElement('div');
                itemDetails.classList.add('flex', 'items-center');

                const itemImage = document.createElement('img');
                itemImage.src = item.image;
                itemImage.alt = item.name;
                itemImage.classList.add('w-16', 'h-16', 'rounded-md', 'mr-4');

                const itemNameQuantity = document.createElement('div');
                itemNameQuantity.classList.add('flex', 'flex-col');
                const itemName = document.createElement('span');
                itemName.textContent = item.name;
                itemName.classList.add('text-gray-900', 'font-semibold');
                const itemQuantity = document.createElement('span');
                itemQuantity.textContent = `Quantity: ${item.quantity}`;
                itemQuantity.classList.add('text-gray-700');
                itemNameQuantity.appendChild(itemName);
                itemNameQuantity.appendChild(itemQuantity);

                itemDetails.appendChild(itemImage);
                itemDetails.appendChild(itemNameQuantity);

                const itemPrice = document.createElement('span');
                itemPrice.textContent = `$${(item.price * item.quantity).toFixed(2)}`;
                itemPrice.classList.add('text-gray-900', 'font-semibold');

                itemElement.appendChild(itemDetails);
                itemElement.appendChild(itemPrice);
                orderSummaryElement.appendChild(itemElement);

                orderTotal += item.price * item.quantity;
            });

            orderTotalElement.textContent = orderTotal.toFixed(2);
            paymentIdElement.textContent = simulatedPaymentId; // Set the payment ID
        }

        // Initial setup
        displayOrderSummary();