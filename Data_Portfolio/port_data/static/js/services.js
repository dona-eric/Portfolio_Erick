// pour les services

document.addEventListener('DOMContentLoaded', function() {
    // Effet de chargement
    const loader = document.querySelector('.loader');
    if (loader) {
      window.addEventListener('load', () => {
        loader.classList.add('loaded');
        setTimeout(() => {
          loader.remove();
        }, 500);
      });
    }
  });
    
    // Validation de formulaire
    const form = document.querySelector('form');
    if (form) {
      form.addEventListener('submit', (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      });
    }
  