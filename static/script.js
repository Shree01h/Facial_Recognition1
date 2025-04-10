// DOM Elements
const traditionalLogin = document.getElementById('traditional-login');
const faceLogin = document.getElementById('face-login');
const faceLoginBtn = document.getElementById('face-login-btn');
const backBtn = document.getElementById('back-btn');
const loginBtn = document.getElementById('login-btn');
const captureBtn = document.getElementById('capture-btn');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const faceMessage = document.getElementById('face-message');
const loginMessage = document.getElementById('login-message');
const forgotPasswordLink = document.getElementById('forgot-password');
const signUpLink = document.getElementById('sign-up');
const rememberMe = document.getElementById('remember-me');
const togglePassword = document.querySelectorAll('.toggle-password');

// Modal Elements
const forgotPasswordModal = document.getElementById('forgot-password-modal');
const signupModal = document.getElementById('signup-modal');
const closeButtons = document.querySelectorAll('.close');

// User Database
const registeredUsers = {
    'admin@example.com': {
        username: 'admin',
        password: 'admin123',
        faceDescriptor: null,
        rememberMe: false
    }
};

// ================== INITIAL SETUP ==================
document.addEventListener('DOMContentLoaded', () => {
    // Load saved credentials
    const savedCredentials = JSON.parse(localStorage.getItem('savedCredentials'));
    if (savedCredentials) {
        document.getElementById('username').value = savedCredentials.username || '';
        document.getElementById('password').value = savedCredentials.password || '';
        rememberMe.checked = true;
    }
    
    initModals();
    initPasswordToggle();
    loadModels();
});

// ================== PASSWORD TOGGLE ==================
function initPasswordToggle() {
    togglePassword.forEach(icon => {
        icon.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            this.textContent = type === 'password' ? '👁' : '👁‍🗨';
        });
    });
}

// ================== FACE RECOGNITION ==================
async function loadModels() {
    try {
        await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
        await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
        await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
        console.log("Models loaded successfully");
    } catch (err) {
        console.error("Failed to load models:", err);
        showMessage(loginMessage, "Error loading face recognition", "error");
    }
}

async function startVideo() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error("Camera error:", err);
        showMessage(faceMessage, "Camera access denied", "error");
    }
}

function stopVideo() {
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
    }
}

// ================== BUTTON HANDLERS ==================
if (faceLoginBtn) {
    faceLoginBtn.addEventListener('click', () => {
        traditionalLogin.style.display = 'none';
        faceLogin.style.display = 'block';
        startVideo();
    });
}

if (backBtn) {
    backBtn.addEventListener('click', () => {
        traditionalLogin.style.display = 'block';
        faceLogin.style.display = 'none';
        stopVideo();
    });
}

if (loginBtn) {
    loginBtn.addEventListener('click', () => {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        if (!username || !password) {
            showMessage(loginMessage, "Please enter both fields", "error");
            return;
        }
        
        const user = Object.values(registeredUsers).find(u => 
            (u.username === username || Object.keys(registeredUsers).includes(username)) && 
            u.password === password
        );
        
        if (user) {
            if (rememberMe.checked) {
                localStorage.setItem('savedCredentials', JSON.stringify({
                    username: username,
                    password: password
                }));
            } else {
                localStorage.removeItem('savedCredentials');
            }
            
            // Store user session
            localStorage.setItem('currentUsername', username);
            
            showMessage(loginMessage, "Login successful!", "success");
        } else {
            showMessage(loginMessage, "Invalid credentials", "error");
        }
    });
}

// ================== FACE CAPTURE ==================
if (captureBtn) {
    captureBtn.addEventListener('click', async () => {
        try {
            const detections = await faceapi.detectAllFaces(
                video, 
                new faceapi.TinyFaceDetectorOptions()
            ).withFaceLandmarks().withFaceDescriptors();
            
            if (detections.length > 0) {
                // Store face descriptor and user data
                const faceDescriptor = Array.from(detections[0].descriptor);
                localStorage.setItem('currentFaceDescriptor', JSON.stringify(faceDescriptor));
                
                const username = document.getElementById('username').value;
                localStorage.setItem('currentUsername', username);
                
                // Update user in database
                const user = Object.values(registeredUsers).find(u => u.username === username);
                if (user) user.faceDescriptor = faceDescriptor;
                
                showMessage(faceMessage, "Face login successful! Redirecting...", "success");
                
                setTimeout(() => {
                    window.location.href = "dashboard.html";
                }, 1500);
            } else {
                showMessage(faceMessage, "No face detected", "error");
            }
        } catch (err) {
            console.error("Face capture error:", err);
            showMessage(faceMessage, "Face capture failed", "error");
        }
    });
}

// ================== MODAL FUNCTIONS ==================
function initModals() {
    // Forgot Password
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', (e) => {
            e.preventDefault();
            forgotPasswordModal.style.display = 'block';
        });
    }
    
    // Sign Up
    if (signUpLink) {
        signUpLink.addEventListener('click', (e) => {
            e.preventDefault();
            signupModal.style.display = 'block';
        });
    }
    
    // Close modals
    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            forgotPasswordModal.style.display = 'none';
            signupModal.style.display = 'none';
        });
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === forgotPasswordModal) forgotPasswordModal.style.display = 'none';
        if (e.target === signupModal) signupModal.style.display = 'none';
    });
    
    // Reset Password
    const resetBtn = document.getElementById('reset-btn');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            const email = document.getElementById('reset-email').value;
            if (email && registeredUsers[email]) {
                showMessage(document.getElementById('reset-message'), 
                    "Password reset link sent to your email", "success");
                setTimeout(() => forgotPasswordModal.style.display = 'none', 2000);
            } else {
                showMessage(document.getElementById('reset-message'), 
                    "Email not registered", "error");
            }
        });
    }
    
    // Register New Account
    const signupBtn = document.getElementById('signup-btn');
    if (signupBtn) {
        signupBtn.addEventListener('click', () => {
            const username = document.getElementById('signup-username').value;
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const confirm = document.getElementById('signup-confirm').value;
            
            if (!username || !email || !password || !confirm) {
                showMessage(document.getElementById('signup-message'), 
                    "Please fill all fields", "error");
                return;
            }
            
            if (password !== confirm) {
                showMessage(document.getElementById('signup-message'), 
                    "Passwords don't match", "error");
                return;
            }
            
            if (registeredUsers[email]) {
                showMessage(document.getElementById('signup-message'), 
                    "Email already registered", "error");
                return;
            }
            
            registeredUsers[email] = {
                username: username,
                password: password,
                faceDescriptor: null
            };
            
            showMessage(document.getElementById('signup-message'), 
                "Account created successfully!", "success");
            
            setTimeout(() => signupModal.style.display = 'none', 2000);
        });
    }
}

// ================== HELPER FUNCTIONS ==================
function showMessage(element, message, type) {
    if (!element) return;
    
    element.textContent = message;
    element.className = `message ${type}`;
    setTimeout(() => {
        if (element.textContent === message) {
            element.textContent = '';
            element.className = 'message';
        }
    }, 5000);
}


//changes for connecting flask request to tkinter GUI
document.getElementById("login-btn").addEventListener("click", async () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    const result = await response.json();
    const message = document.getElementById("login-message");

    if (result.status === "success") {
        message.innerText = "Login successful!";
    } else {
        message.innerText = result.message;
    }
});