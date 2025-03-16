document.addEventListener('DOMContentLoaded', function() {
    // Ajouter une classe pour indiquer que le DOM est chargé
    document.body.classList.add('dom-loaded');
  
    // Animation de chargement
    const loader = document.querySelector('.loader');
    if (loader) {
      window.addEventListener('load', () => {
        loader.classList.add('loaded');
        setTimeout(() => {
          loader.remove();
        }, 500);
      });
    }
  
    // Gestion des liens externes
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    externalLinks.forEach(link => {
      link.setAttribute('rel', 'noopener noreferrer');
      link.setAttribute('target', '_blank');
    });
  
    // Effet de survol pour les cartes
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
      card.addEventListener('mouseover', () => {
        card.classList.add('hovered');
      });
      card.addEventListener('mouseout', () => {
        card.classList.remove('hovered');
      });
    });
  
    // Validation de formulaires
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
      form.addEventListener('submit', (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      });
    });
  
    // Scroll progress bar
    const progressBar = document.createElement('div');
    progressBar.classList.add('scroll-progress');
    document.body.prepend(progressBar);
  
    window.addEventListener('scroll', () => {
      let scroll = document.documentElement.scrollTop;
      let height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      let progress = (scroll / height) * 100;
      progressBar.style.width = `${progress}%`;
    });
  
    // Ajout d'un bouton "Retour en haut"
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '↑';
    backToTopButton.classList.add('back-to-top');
    document.body.appendChild(backToTopButton);
  
    window.addEventListener('scroll', () => {
      if (document.documentElement.scrollTop > 300) {
        backToTopButton.style.display = 'block';
      } else {
        backToTopButton.style.display = 'none';
      }
    });
  
    backToTopButton.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  
    // Dark mode toggle
    const darkModeToggle = document.createElement('button');
    darkModeToggle.innerHTML = '🌙';
    darkModeToggle.classList.add('dark-mode-toggle');
    document.body.appendChild(darkModeToggle);
  
    darkModeToggle.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      if (document.body.classList.contains('dark-mode')) {
        darkModeToggle.innerHTML = '☀️';
        localStorage.setItem('dark-mode', 'enabled');
      } else {
        darkModeToggle.innerHTML = '🌙';
        localStorage.setItem('dark-mode', 'disabled');
      }
    });
  
    if (localStorage.getItem('dark-mode') === 'enabled') {
      document.body.classList.add('dark-mode');
      darkModeToggle.innerHTML = '☀️';
    }
  });
  