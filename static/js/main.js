// Toggle Save Property (AJAX)
function toggleSave(slug) {
  const csrfToken = document.cookie.split(';')
    .find(c => c.trim().startsWith('csrftoken='))
    ?.split('=')[1];

  fetch(`/properties/${slug}/save/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
  .then(r => r.json())
  .then(data => {
    showToast(data.message, data.saved ? 'success' : 'info');
  })
  .catch(() => {
    window.location.href = '/accounts/login/';
  });
}

// Toast notification
function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `fixed bottom-24 right-6 z-50 px-5 py-3 rounded-xl shadow-lg text-sm font-medium animate-slide-up transition-all
    ${type === 'success' ? 'bg-emerald-500 text-white' : 'bg-gray-800 text-white'}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

// Image gallery click
document.addEventListener('DOMContentLoaded', function () {
  // Thumbnail click to swap main image
  document.querySelectorAll('[data-gallery-thumb]').forEach(thumb => {
    thumb.addEventListener('click', function () {
      const mainImg = document.getElementById('main-image');
      if (mainImg) {
        mainImg.src = this.src;
      }
      // Active state
      document.querySelectorAll('[data-gallery-thumb]').forEach(t => t.classList.remove('border-teal-500'));
      this.classList.add('border-teal-500');
    });
  });
});
