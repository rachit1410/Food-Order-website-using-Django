function switchTab(tabId) {
            const tabs = ['profile', 'orders', 'settings'];
            tabs.forEach(tab => {
                const tabElement = document.getElementById(`${tab}-tab`);
                const contentElement = document.getElementById(`${tab}-content`);
                if (tab === tabId) {
                    tabElement.classList.remove('tab-inactive');
                    tabElement.classList.add('tab-active');
                    contentElement.classList.remove('hidden');
                } else {
                    tabElement.classList.remove('tab-active');
                    tabElement.classList.add('tab-inactive');
                    contentElement.classList.add('hidden');
                }
            });
             // Update appearance for dark mode
            const isDarkMode = document.body.classList.contains('dark');
            tabs.forEach(tab => {
                const tabElement = document.getElementById(`${tab}-tab`);
                if (tabElement.classList.contains('tab-active')) {
                    tabElement.classList.add(isDarkMode ? 'dark' : '');
                } else {
                    tabElement.classList.remove(isDarkMode ? 'dark' : '');
                }
            });
        }

        document.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();

            const editProfileButton = document.getElementById('edit-profile-button');
            const saveProfileButton = document.getElementById('save-profile-button');
            const cancelProfileButton = document.getElementById('cancel-profile-button');
            const profileEditView = document.getElementById('profile-edit-view');
            const profileDisplayView = document.getElementById('profile-display-view');
            const editProfileButtonDisplay = document.getElementById('edit-profile-button-display');


            if (editProfileButton) {
                editProfileButton.addEventListener('click', () => {
                    profileEditView.classList.remove('hidden');
                    profileDisplayView.classList.add('hidden');
                    saveProfileButton.classList.remove('hidden');
                    cancelProfileButton.classList.remove('hidden');
                    editProfileButton.classList.add('hidden');
                });
            }

             if (editProfileButtonDisplay) {
                editProfileButtonDisplay.addEventListener('click', () => {
                    profileEditView.classList.remove('hidden');
                    profileDisplayView.classList.add('hidden');
                    saveProfileButton.classList.remove('hidden');
                    cancelProfileButton.classList.remove('hidden');
                    editProfileButton.classList.add('hidden');
                });
            }


            if (saveProfileButton) {
                saveProfileButton.addEventListener('click', () => {
                    const firstNameInput = document.getElementById('first-name');
                    const lastNameInput = document.getElementById('last-name');
                    const phoneInput = document.getElementById('phone');
                    const cityInput = document.getElementById('city');
                    const stateInput = document.getElementById('state');
                    const countryInput = document.getElementById('country');

                    const firstName = firstNameInput.value;
                    const lastName = lastNameInput.value;
                    const phone = phoneInput.value;
                    const city = cityInput.value;
                    const state = stateInput.value;
                    const country = countryInput.value;


                    const firstNameDisplay = document.querySelector('#profile-display-view span:nth-child(2)');
                    const lastNameDisplay = document.querySelector('#profile-display-view span:nth-child(4)');
                    const phoneDisplay = document.querySelector('#profile-display-view span:nth-child(6)');
                    const cityDisplay = document.querySelector('#profile-display-view span:nth-child(8)');
                    const stateDisplay = document.querySelector('#profile-display-view span:nth-child(10)');
                    const countryDisplay = document.querySelector('#profile-display-view span:nth-child(12)');

                    firstNameDisplay.textContent = firstName;
                    lastNameDisplay.textContent = lastName;
                    phoneDisplay.textContent = phone;
                    cityDisplay.textContent = city;
                    stateDisplay.textContent = state;
                    countryDisplay.textContent = country;

                    profileEditView.classList.add('hidden');
                    profileDisplayView.classList.remove('hidden');
                    saveProfileButton.classList.add('hidden');
                    cancelProfileButton.classList.add('hidden');
                    editProfileButton.classList.remove('hidden');
                });
            }

            if (cancelProfileButton) {
                cancelProfileButton.addEventListener('click', () => {
                    profileEditView.classList.add('hidden');
                    profileDisplayView.classList.remove('hidden');
                    saveProfileButton.classList.add('hidden');
                    cancelProfileButton.classList.add('hidden');
                    editProfileButton.classList.remove('hidden');
                });
            }
        });