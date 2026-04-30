// ==============================
// Back to Top Button Script
// ==============================

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function () {
  // Create the button dynamically
  const backToTopBtn = document.createElement('button');
  backToTopBtn.id = 'backToTopBtn';
  backToTopBtn.className = 'back-to-top';
  backToTopBtn.title = 'Back to top';
  backToTopBtn.textContent = '↑';
  document.body.appendChild(backToTopBtn);

  // Show or hide when scrolling
  window.addEventListener('scroll', function () {
    if (document.body.scrollTop > 250 || document.documentElement.scrollTop > 250) {
      backToTopBtn.style.display = 'block';
    } else {
      backToTopBtn.style.display = 'none';
    }
  });

  // Smooth scroll to top when clicked
  backToTopBtn.addEventListener('click', function () {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
});
