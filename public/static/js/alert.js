document.addEventListener('DOMContentLoaded', () => {
            const alertBar = document.getElementById('myAlertBar');
            const alertBarContent = alertBar.querySelector('.alert-bar');
            const alertMessage = alertBar.querySelector('.alert-message');
            const alertIconPath = alertBar.querySelector('.alert-icon path');
            const closeButton = document.getElementById('closeAlert');

            let autoHideTimeout; // Variable to store the timeout ID

            // Function to show the alert bar with dynamic type and message
            const showAlert = (type = 'info', message = 'This is a sample alert message! It will disappear automatically.') => {
                // Reset classes for background and text color
                alertBarContent.classList.remove('bg-blue-500', 'bg-green-500', 'bg-yellow-500', 'bg-red-500', 'text-white', 'text-gray-800');

                // Apply new classes and update icon based on type
                switch (type) {
                    case 'success':
                        alertBarContent.classList.add('bg-green-500', 'text-white');
                        // Checkmark circle icon (from Heroicons)
                        alertIconPath.setAttribute('d', 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z');
                        break;
                    case 'warning':
                        alertBarContent.classList.add('bg-yellow-500', 'text-gray-800'); // Use text-gray-800 for better contrast on yellow
                        // Exclamation triangle icon (from Heroicons)
                        alertIconPath.setAttribute('d', 'M8.257 3.099c.765-1.36 2.722-1.36 3.486 0L19.75 15.3A1 1 0 0119 17H5a1 1 0 01-.75-1.7L8.257 3.099zM10 13a1 1 0 100-2 1 1 0 000 2zm0 4a1 1 0 100-2 1 1 0 000 2z');
                        break;
                    case 'error':
                        alertBarContent.classList.add('bg-red-500', 'text-white');
                        // X circle icon (from Heroicons)
                        alertIconPath.setAttribute('d', 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z');
                        break;
                    case 'info':
                    default:
                        alertBarContent.classList.add('bg-blue-500', 'text-white');
                        // Info circle icon (from Heroicons)
                        alertIconPath.setAttribute('d', 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2h2a1 1 0 000-2H9zm2 4a1 1 0 10-2 0 1 1 0 002 0z');
                        break;
                }

                alertMessage.textContent = message; // Update message text
                alertBar.classList.remove('alert-hidden');
                alertBar.classList.add('alert-visible');

                // Clear any existing auto-hide timeout
                if (autoHideTimeout) {
                    clearTimeout(autoHideTimeout);
                }

                // Set a new auto-hide timeout for 5 seconds (5000 milliseconds)
                autoHideTimeout = setTimeout(hideAlert, 5000);
            };

            // Function to hide the alert bar
            const hideAlert = () => {
                alertBar.classList.remove('alert-visible');
                alertBar.classList.add('alert-hidden');
                // Clear the timeout when hidden manually or automatically
                if (autoHideTimeout) {
                    clearTimeout(autoHideTimeout);
                    autoHideTimeout = null;
                }
            };

            // --- Django Messages Integration Logic ---
            const djangoMessagesDataElement = document.getElementById('django-messages-data');
            if (djangoMessagesDataElement) {
                try {
                    const messages = JSON.parse(djangoMessagesDataElement.textContent);
                    if (Array.isArray(messages) && messages.length > 0) {
                        let delay = 0;
                        messages.forEach(msg => {
                            // Show each message with a slight delay
                            setTimeout(() => {
                                if (msg.type && msg.message) {
                                    showAlert(msg.type, msg.message);
                                } else {
                                    console.warn('Invalid message structure from Django:', msg);
                                }
                            }, delay);
                            delay += 1500; // Add 1.5 second delay for each subsequent message
                        });
                    }
                } catch (e) {
                    console.error('Error parsing Django messages data:', e);
                }
            }

            // Event listener for the close button
            closeButton.addEventListener('click', hideAlert);
        });