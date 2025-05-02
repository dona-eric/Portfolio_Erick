// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    // Toggle du menu mobile
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');
    
    if (navbarToggle && navbarMenu) {
      navbarToggle.addEventListener('click', function() {
        navbarMenu.classList.toggle('active');
      });
    }
    
    // Navigation active
    const navLinks = document.querySelectorAll('.navbar-link');
    const sections = document.querySelectorAll('section');
    
    function setActiveNavLink() {
      let current = '';
      sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop && pageYOffset < sectionTop + sectionHeight) {
          current = section.getAttribute('id');
        }
      });
      
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + current) {
          link.classList.add('active');
        }
      });
    }
    
    // Écouteur d'événement pour le défilement
    window.addEventListener('scroll', function() {
      setActiveNavLink();
      
      // Navbar effet de scrolling
      const navbar = document.querySelector('.navbar');
      if (window.scrollY > 50) {
        navbar.style.padding = '0.5rem 0';
        navbar.style.background = 'rgba(10, 10, 10, 0.95)';
      } else {
        navbar.style.padding = '1rem 0';
        navbar.style.background = 'rgba(10, 10, 10, 0.8)';
      }
      
      // Animation des éléments au défilement
      const animateElements = document.querySelectorAll('.animate-on-scroll');
      animateElements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        if (elementPosition < windowHeight - 100) {
          element.classList.add('animate-fade-up');
        }
      });
    });
    
    // Ajouter une classe animate-on-scroll aux éléments à animer
    document.querySelectorAll('section').forEach(section => {
      section.classList.add('animate-on-scroll');
    });
  });
  


  


  document.addEventListener('DOMContentLoaded', function() {
    // Effet de scroll sur la navbar
    const navbar = document.querySelector('.navbar');
    if (navbar) {
      window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
          navbar.classList.add('scrolled');
        } else {
          navbar.classList.remove('scrolled');
        }
      });
    }
    
    // Toggle du menu mobile
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
      navbarToggler.addEventListener('click', function() {
        navbarCollapse.classList.toggle('show');
        const expanded = navbarToggler.getAttribute('aria-expanded') === 'true' || false;
        navbarToggler.setAttribute('aria-expanded', !expanded);
      });
      
      // Fermer le menu quand un lien est cliqué
      document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
          navbarCollapse.classList.remove('show');
          navbarToggler.setAttribute('aria-expanded', 'false');
        });
      });
    }
  });
  document.addEventListener('DOMContentLoaded', () => {
    showMessage("Bonjour ! Je suis l'assistant IA de Eric KOULODJI. Souhaites-tu en savoir plus sur mon parcours, mes projets ou mes compétences ?", 'bot');
});

function showMessage(text, sender) {
    const chat = document.getElementById('chat-messages');
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender}`;
    bubble.innerText = text;
    chat.appendChild(bubble);
    chat.scrollTop = chat.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById('user-input');
    const text = input.value.trim();
    if (!text) return;

    showMessage(text, 'user');
    input.value = '';

    fetch('/ask-ai/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'  // Assure-toi que tu as le token dans ton template
        },
        body: JSON.stringify({ question: text })
    })
    .then(response => response.json())
    .then(data => {
        showMessage(data.answer, 'bot');
    })
    .catch(error => {
        console.error('Erreur :', error);
        showMessage("Désolé, une erreur est survenue.", 'bot');
    });
}
  document.getElementById('send-button').addEventListener('click', sendMessage);
  document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
      sendMessage();
    }
  });
// Fonction pour afficher le message de l'assistant
function showMessage(text, sender) {
    const chat = document.getElementById('chat-messages');
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender}`;
    bubble.innerText = text;
    chat.appendChild(bubble);
    chat.scrollTop = chat.scrollHeight;
}
// Fonction pour envoyer le message de l'utilisateur
function sendMessage() {
    const input = document.getElementById('user-input');
    const text = input.value.trim();
    if (!text) return;

    showMessage(text, 'user');
    input.value = '';

    fetch('/ask-ai/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'  // Assure-toi que tu as le token dans ton template
        },
        body: JSON.stringify({ question: text })
    })
    .then(response => response.json())
    .then(data => {
        showMessage(data.answer, 'bot');
    })
    .catch(error => {
        console.error('Erreur :', error);
        showMessage("Désolé, une erreur est survenue.", 'bot');
    });
}
// Écouteur d'événement pour le bouton d'envoi
document.getElementById('send-button').addEventListener('click', sendMessage);
// Écouteur d'événement pour la touche "Entrée"
