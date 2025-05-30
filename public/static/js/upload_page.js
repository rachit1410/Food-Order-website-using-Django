 const excelFileInput = document.getElementById('excelFileInput');
        const uploadButton = document.getElementById('uploadButton');
        const uploadMessage = document.getElementById('uploadMessage');
        const currentUploadSection = document.getElementById('currentUploadSection');
        const uploadFileName = document.getElementById('uploadFileName');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const uploadStatus = document.getElementById('uploadStatus');
        const recentUploadsList = document.getElementById('recentUploadsList');
        const noRecentUploads = document.getElementById('noRecentUploads');
        const currentUploadPercentageDisplay = document.getElementById('currentUploadPercentageDisplay');

        // Function to format date and time
        function formatDateTime(date) {
            const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true };
            return new Intl.DateTimeFormat('en-IN', options).format(date);
        }

        // Function to add an upload entry to the recent uploads list
        function addRecentUploadEntry(fileName, status) {
            const now = new Date();
            const dateTimeString = formatDateTime(now);

            const entryDiv = document.createElement('div');
            entryDiv.className = 'flex justify-between items-center bg-white p-3 rounded-md shadow-sm border border-gray-200';

            const statusColor = status === 'Completed' ? 'text-green-600' : 'text-red-600';

            entryDiv.innerHTML = `
                <span class="font-medium text-gray-800">${fileName}</span>
                <span class="text-sm text-gray-500">Uploaded: ${dateTimeString}</span>
                <span class="text-sm ${statusColor} font-semibold">${status}</span>
            `;
            recentUploadsList.prepend(entryDiv); // Add to the top of the list

            // Hide "No recent uploads" message if there are uploads
            if (recentUploadsList.children.length > 0) {
                noRecentUploads.classList.add('hidden');
            }
        }

        // Function to simulate an upload using XMLHttpRequest for progress tracking
        function simulateUploadWithProgress(file) {
            currentUploadSection.classList.remove('hidden');
            uploadFileName.textContent = file.name;
            progressBar.style.width = '0%';
            progressText.textContent = '0%';
            currentUploadPercentageDisplay.textContent = '0%';
            uploadStatus.textContent = 'Uploading...';
            uploadStatus.classList.remove('text-green-600', 'text-red-600');
            uploadStatus.classList.add('text-blue-600'); // Indicate ongoing

            const xhr = new XMLHttpRequest();
            // Simulate a POST request to a dummy URL
            xhr.open('POST', 'https://jsonplaceholder.typicode.com/posts', true);

            // Set up event listener for upload progress
            xhr.upload.onprogress = function(event) {
                if (event.lengthComputable) {
                    const percentComplete = Math.round((event.loaded / event.total) * 100);
                    progressBar.style.width = `${percentComplete}%`;
                    progressText.textContent = `${percentComplete}%`;
                    currentUploadPercentageDisplay.textContent = `${percentComplete}%`;
                }
            };

            // Set up event listener for when the upload is complete
            xhr.onload = function() {
                if (xhr.status >= 200 && xhr.status < 300) {
                    // Simulate success
                    uploadStatus.textContent = 'Upload Completed Successfully!';
                    uploadStatus.classList.remove('text-blue-600');
                    uploadStatus.classList.add('text-green-600');
                    addRecentUploadEntry(file.name, 'Completed');
                } else {
                    // Simulate failure
                    uploadStatus.textContent = `Upload Failed. Status: ${xhr.status}`;
                    uploadStatus.classList.remove('text-blue-600');
                    uploadStatus.classList.add('text-red-600');
                    addRecentUploadEntry(file.name, 'Failed');
                }
                // Optionally hide the progress section after a delay
                setTimeout(() => {
                    currentUploadSection.classList.add('hidden');
                    uploadMessage.classList.add('hidden');
                    currentUploadPercentageDisplay.textContent = '0%'; // Clear percentage after hiding
                }, 3000);
            };

            // Set up event listener for upload errors
            xhr.onerror = function() {
                uploadStatus.textContent = 'Upload Failed due to network error.';
                uploadStatus.classList.remove('text-blue-600');
                uploadStatus.classList.add('text-red-600');
                addRecentUploadEntry(file.name, 'Failed');
                setTimeout(() => {
                    currentUploadSection.classList.add('hidden');
                    uploadMessage.classList.add('hidden');
                    currentUploadPercentageDisplay.textContent = '0%';
                }, 3000);
            };

            // Create a FormData object to send the file
            const formData = new FormData();
            formData.append('excelFile', file); // 'excelFile' would be the field name on the server

            // Send the request
            xhr.send(formData);
        }

        // Event listener for the upload button
        uploadButton.addEventListener('click', () => {
            const file = excelFileInput.files[0];
            if (file) {
                uploadMessage.classList.add('hidden'); // Hide previous messages
                simulateUploadWithProgress(file); // Call the new function
            } else {
                uploadMessage.textContent = 'Please select an Excel or CSV file to upload.';
                uploadMessage.classList.remove('hidden');
                uploadMessage.classList.remove('text-green-700');
                uploadMessage.classList.add('text-red-700');
            }
        });

        // Initial check for recent uploads placeholder
        if (recentUploadsList.children.length === 0) {
            noRecentUploads.classList.remove('hidden');
        }