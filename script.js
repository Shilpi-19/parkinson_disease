// document.addEventListener('DOMContentLoaded', () => {
//     const uploadArea = document.getElementById('uploadArea');
//     const uploadBtn = document.getElementById('uploadBtn');
//     const fileInput = document.getElementById('fileInput');
//     const filesList = document.getElementById('filesList');
    

//     // Click the hidden file input when the 'Browse' link is clicked
//     uploadArea.addEventListener('click', () => {
//         fileInput.click();
//     });

//     // Handle file input change
//     fileInput.addEventListener('change', (event) => {
//         const files = event.target.files;
//         displayFiles(files);
//     });

//     // Display the selected files
//     function displayFiles(files) {
//         filesList.innerHTML = ''; // Clear the list

//         Array.from(files).forEach(file => {
//             const fileItem = document.createElement('div');
//             fileItem.className = 'file-item';
//             fileItem.textContent = file.name; // Add other file details as needed
//             filesList.appendChild(fileItem);
//         });
//     }

//     // Handle the file upload button
//     uploadBtn.addEventListener('click', () => {
//         // Here you would normally handle the actual file upload.
//         alert('Files ready for upload!');
//     });
// });

document.addEventListener('DOMContentLoaded', function () {
    // Login form submission
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Here you can perform login authentication using email and password
        // For simplicity, I'm just logging them
        console.log('Email:', email);
        console.log('Password:', password);

        // Redirect to the home page after successful login
        window.location.href = 'home.html';
    });

    // Signup form submission
    const registerForm = document.getElementById('register-form');
    registerForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Here you can perform signup authentication using name, email, and password
        // For simplicity, I'm just logging them
        console.log('Name:', name);
        console.log('Email:', email);
        console.log('Password:', password);

        // Redirect to the login page after successful signup
        window.location.href = 'login.html';
    });

    // Functionality for voice input on the home page (you need to implement this)
    // Example: You can use Web Speech API for voice recognition
    // https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
    const voiceInputButton = document.getElementById('voice-input-button');
    voiceInputButton.addEventListener('click', function () {
        // Implement your voice input functionality here
        console.log('Voice input functionality will be implemented here');
    });

    // File upload functionality
    const uploadArea = document.getElementById('uploadArea');
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInput = document.getElementById('fileInput');
    const filesList = document.getElementById('filesList');

    // Click the hidden file input when the 'Browse' link is clicked
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle file input change
    fileInput.addEventListener('change', (event) => {
        const files = event.target.files;
        displayFiles(files);
    });

    // Display the selected files
    function displayFiles(files) {
        filesList.innerHTML = ''; // Clear the list

        Array.from(files).forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.textContent = file.name; // Add other file details as needed
            filesList.appendChild(fileItem);
        });
    }

    // Handle the file upload button
    uploadBtn.addEventListener('click', () => {
        // Here you would normally handle the actual file upload.
        alert('Files ready for upload!');
    });
});
