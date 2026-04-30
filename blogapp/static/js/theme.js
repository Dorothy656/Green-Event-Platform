class ThemeManager {
  constructor() {
    // Get DOM elements - must match HTML structure
    this.themeToggle = document.getElementById('theme-toggle');
    this.bgUpload = document.getElementById('bg-upload');

    // Initialize theme
    this.init();

    // Bind events
    this.bindEvents();
  }

  // Initialize theme and background settings
  init() {
    // Load saved theme from localStorage
    const savedTheme = localStorage.getItem('theme') || 'light';
    const savedBg = localStorage.getItem('custom-bg');

    // Apply theme
    if (savedTheme === 'dark') {
      document.body.classList.add('dark-theme');
    }

    // Apply custom background (if any)
    if (savedBg) {
      document.body.style.setProperty('--bg-image', `url(${savedBg})`);
    }
  }

  // Bind event listeners
  bindEvents() {
    // Theme toggle button - single switch
    if (this.themeToggle) {
      this.themeToggle.addEventListener('click', () => {
        this.toggleTheme();
      });
    }

    // Custom background upload
    if (this.bgUpload) {
      this.bgUpload.addEventListener('change', (e) => {
        this.uploadCustomBackground(e.target.files[0]);
      });
    }
  }

  // Toggle theme (single method)
  toggleTheme() {
    // Toggle dark-theme class
    const isDark = document.body.classList.toggle('dark-theme');
    // Save theme to localStorage
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    // Icon switch is handled by CSS automatically
  }

  // Upload custom background
  uploadCustomBackground(file) {
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file.');
      return;
    }

    const reader = new FileReader();

    reader.onload = (e) => {
      // Set background image
      document.body.style.setProperty('--bg-image', `url(${e.target.result})`);
      // Save custom background to localStorage
      localStorage.setItem('custom-bg', e.target.result);
    };

    reader.readAsDataURL(file);
  }
}

// Initialize theme manager after DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new ThemeManager();
});