const cardNumberInput = document.getElementById('card-number');
        const expiryDateInput = document.getElementById('expiry-date');
        const cvvInput = document.getElementById('cvv');
        const cardholderNameInput = document.getElementById('cardholder-name');
        const cardNumberError = document.getElementById('card-number-error');
        const expiryDateError = document.getElementById('expiry-date-error');
        const cvvError = document.getElementById('cvv-error');
        const cardholderNameError = document.getElementById('cardholder-name-error');
        const paymentMessage = document.getElementById('payment-message');
        const paymentMessageText = document.getElementById('payment-message-text');

        function validateCardDetails() {
            let isValid = true;
            const cardNumber = cardNumberInput.value.trim();
            const expiryDate = expiryDateInput.value.trim();
            const cvv = cvvInput.value.trim();
            const cardholderName = cardholderNameInput.value.trim();

            cardNumberError.classList.add('hidden');
            expiryDateError.classList.add('hidden');
            cvvError.classList.add('hidden');
            cardholderNameError.classList.add('hidden');

            if (!cardNumber) {
                cardNumberError.textContent = 'Card number is required';
                cardNumberError.classList.remove('hidden');
                isValid = false;
            } else if (!/^\d{4} \d{4} \d{4} \d{4}$/.test(cardNumber)) {
                cardNumberError.textContent = 'Invalid card number format';
                cardNumberError.classList.remove('hidden');
                isValid = false;
            }

            if (!expiryDate) {
                expiryDateError.textContent = 'Expiry date is required';
                expiryDateError.classList.remove('hidden');
                isValid = false;
            } else if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test(expiryDate)) {
                expiryDateError.textContent = 'Invalid expiry date format';
                expiryDateError.classList.remove('hidden');
                isValid = false;
            }

            if (!cvv) {
                cvvError.textContent = 'CVV is required';
                cvvError.classList.remove('hidden');
                isValid = false;
            } else if (!/^\d{3}$/.test(cvv)) {
                cvvError.textContent = 'Invalid CVV format';
                cvvError.classList.remove('hidden');
                isValid = false;
            }

            if (!cardholderName) {
                cardholderNameError.textContent = 'Cardholder name is required';
                cardholderNameError.classList.remove('hidden');
                isValid = false;
            }

            if (isValid) {
                // Simulate payment processing
                paymentMessage.classList.remove('hidden');
                paymentMessageText.textContent = `Processing payment for card ending with ${cardNumber.slice(-4)}...`;

                setTimeout(() => {
                    paymentMessageText.textContent = 'Payment successful!';
                    paymentMessageText.classList.remove('text-gray-900');
                    paymentMessageText.classList.add('text-green-600');
                    // In a real application, you would redirect to a confirmation page
                    // window.location.href = 'order-confirmation.html';
                }, 3000); // Simulate 3 seconds processing time
            }
        }