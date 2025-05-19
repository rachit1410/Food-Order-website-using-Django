        const upiQrRadio = document.getElementById('upi-qr');
        const upiIdRadio = document.getElementById('upi-id');
        const qrCodeSection = document.getElementById('qr-code-section');
        const upiIdSection = document.getElementById('upi-id-section');
        const upiIdInput = document.getElementById('upi-id-input');
        const upiIdError = document.getElementById('upi-id-error');
        const paymentMessage = document.getElementById('payment-message');
        const paymentMessageText = document.getElementById('payment-message-text');
        const qrCodePlaceholder = document.getElementById('qr-code-placeholder'); // Get the QR code placeholder

        upiQrRadio.addEventListener('change', () => {
            qrCodeSection.classList.remove('hidden');
            upiIdSection.classList.add('hidden');
            paymentMessage.classList.add('hidden');
        });

        upiIdRadio.addEventListener('change', () => {
            qrCodeSection.classList.add('hidden');
            upiIdSection.classList.remove('hidden');
            paymentMessage.classList.add('hidden');
        });

        function validateAndPay() {
            const upiIdValue = upiIdInput.value.trim();
            upiIdError.classList.add('hidden');

            if (!upiIdValue) {
                upiIdError.textContent = 'UPI ID is required';
                upiIdError.classList.remove('hidden');
                return;
            } else if (!/^[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}$/.test(upiIdValue)) {
                upiIdError.textContent = 'Invalid UPI ID format';
                upiIdError.classList.remove('hidden');
                return;
            }

            // Simulate payment processing
            paymentMessage.classList.remove('hidden');
            paymentMessageText.textContent = `Processing payment for UPI ID: ${upiIdValue}...`;

            setTimeout(() => {
                paymentMessageText.textContent = 'Payment successful!';
                paymentMessageText.classList.remove('text-gray-900');
                paymentMessageText.classList.add('text-green-600');
                // In a real application, you would redirect to a confirmation page
                // window.location.href = 'order-confirmation.html';
            }, 3000); // Simulate 3 seconds processing time
        }

        // Generate a dummy QR code on page load (for demonstration purposes)
        function generateDummyQRCode() {
            const dummyQRCode = "https://api.qrserver.com/v1/create-qr-code/?size=256x256&data=upi://pay?pa=yourname@bank&pn=MerchantName&am=100.00"; // Replace with actual data
            const qrCodeImg = document.createElement('img');
            qrCodeImg.src = dummyQRCode;
            qrCodeImg.alt = "UPI Payment QR Code";
            qrCodeImg.classList.add('rounded-md');
            qrCodePlaceholder.innerHTML = ''; // Clear placeholder
            qrCodePlaceholder.appendChild(qrCodeImg); // Append the image
        }

        // Generate dummy QR code when the page loads or when the QR code option is selected
        if (upiQrRadio.checked) {
            generateDummyQRCode();
        }

        upiQrRadio.addEventListener('change', generateDummyQRCode);