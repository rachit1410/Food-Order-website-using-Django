 const collectionsData = [
            { name: "Fresh Produce", description: "Seasonal fruits and vegetables, picked fresh daily.", itemCount: 150, color: "green" },
            { name: "Dairy & Bakery", description: "Milk, cheese, yogurt, and freshly baked goods.", itemCount: 80, color: "yellow" },
            { name: "Pantry Staples", description: "Rice, pasta, oils, spices, and canned goods.", itemCount: 200, color: "purple" },
            { name: "Beverages", description: "Juices, sodas, coffee, and tea selections.", itemCount: 65, color: "red" },
            { name: "Frozen Foods", description: "Ready meals, frozen vegetables, and desserts.", itemCount: 95, color: "blue" },
            { name: "Household Essentials", description: "Cleaning supplies, paper products, and more.", itemCount: 120, color: "gray" }
        ];

        const collectionsList = document.getElementById('collectionsList');
        const noCollectionsMessage = document.getElementById('noCollections');

        // Function to render collections
        function renderCollections() {
            collectionsList.innerHTML = ''; // Clear existing content
            if (collectionsData.length === 0) {
                noCollectionsMessage.classList.remove('hidden');
                return;
            } else {
                noCollectionsMessage.classList.add('hidden');
            }

            collectionsData.forEach(collection => {
                const collectionCard = document.createElement('div');
                collectionCard.className = `bg-white rounded-lg shadow-md p-5 border border-gray-200 hover:shadow-lg transition-shadow duration-300`;
                collectionCard.innerHTML = `
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">${collection.name}</h3>
                    <p class="text-gray-600 text-sm mb-3">${collection.description}</p>
                    <span class="inline-block bg-${collection.color}-100 text-${collection.color}-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                        ${collection.itemCount} Items
                    </span>
                `;
                collectionsList.appendChild(collectionCard);
            });
        }

        // Initial render
        renderCollections();