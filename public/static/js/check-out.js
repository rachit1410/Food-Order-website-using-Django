        const orderSummaryElement = document.getElementById('order-summary');
        const orderTotalElement = document.getElementById('order-total');
        const orderConfirmation = document.getElementById('order-confirmation');
        const paymentMethodError = document.getElementById('payment-method-error');
        const paymentMethodItems = document.querySelectorAll('.payment-method-item');


        // Sample cart data (replace with actual data from localStorage or an API)
        let cart = [
            { id: 1, name: 'Product 1', price: 19.99, quantity: 2, image: 'https://via.placeholder.com/100' },
            { id: 2, name: 'Product 2', price: 29.99, quantity: 1, image: 'https://via.placeholder.com/100' },
            { id: 3, name: 'Product 3', price: 15.50, quantity: 3, image: 'https://via.placeholder.com/100' },
        ];

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
        }

        function validateForm() {
            let isValid = true;
            const firstName = document.getElementById('first-name').value.trim();
            const lastName = document.getElementById('last-name').value.trim();
            const email = document.getElementById('email').value.trim();
            const address = document.getElementById('address').value.trim();
            const city = document.getElementById('city').value.trim();
            const state = document.getElementById('state').value.trim();
            const zip = document.getElementById('zip').value.trim();
            const paymentMethod = document.querySelector('input[name="payment-method"]:checked');

            const firstNameError = document.getElementById('first-name-error');
            const lastNameError = document.getElementById('last-name-error');
            const emailError = document.getElementById('email-error');
            const addressError = document.getElementById('address-error');
            const cityError = document.getElementById('city-error');
            const stateError = document.getElementById('state-error');
            const zipError = document.getElementById('zip-error');


            firstNameError.classList.add('hidden');
            lastNameError.classList.add('hidden');
            emailError.classList.add('hidden');
            addressError.classList.add('hidden');
            cityError.classList.add('hidden');
            stateError.classList.add('hidden');
            zipError.classList.add('hidden');
            paymentMethodError.classList.add('hidden');


            if (!firstName) {
                firstNameError.textContent = 'First name is required';
                firstNameError.classList.remove('hidden');
                isValid = false;
            }
            if (!lastName) {
                lastNameError.textContent = 'Last name is required';
                lastNameError.classList.remove('hidden');
                isValid = false;
            }
            if (!email) {
                emailError.textContent = 'Email is required';
                emailError.classList.remove('hidden');
                isValid = false;
            } else if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
                emailError.textContent = 'Invalid email format';
                emailError.classList.remove('hidden');
                isValid = false;
            }
            if (!address) {
                addressError.textContent = 'Address is required';
                addressError.classList.remove('hidden');
                isValid = false;
            }
            if (!city) {
                cityError.textContent = 'City is required';
                cityError.classList.remove('hidden');
                isValid = false;
            }
            if (!state) {
                stateError.textContent = 'State is required';
                stateError.classList.remove('hidden');
                isValid = false;
            }
            if (!zip) {
                zipError.textContent = 'ZIP is required';
                zipError.classList.remove('hidden');
                isValid = false;
            }
            if (!paymentMethod) {
                paymentMethodError.textContent = 'Please select a payment method';
                paymentMethodError.classList.remove('hidden');
                isValid = false;
            }
            return isValid;
        }

        function submitOrder() {
            if (validateForm()) {
                // In a real application, you would send the order data to a server
                console.log('Order submitted!');
                orderConfirmation.classList.remove('hidden');
                // Clear the cart (in a real app, you might want to keep a record of the order)
                cart = [];
                displayOrderSummary();
                 setTimeout(() => {
                    orderConfirmation.classList.add('hidden');
                 }, 3000);
            }
        }

        // Initial setup
        displayOrderSummary();

        paymentMethodItems.forEach(item => {
            item.addEventListener('click', () => {
                // Remove 'selected' class from all items
                paymentMethodItems.forEach(el => el.querySelector('label').classList.remove('selected'));
                // Add 'selected' class to the clicked item
                item.querySelector('label').classList.add('selected');
                //update the radio button
                item.querySelector('input[type="radio"]').checked = true;
            });
        });