// main.js
document.addEventListener('DOMContentLoaded', () => {
    // Configuration globale
    const config = {
        scrollOffset: 100,
        animationDuration: 300,
        mobileBreakpoint: 768
    };

    // Initialisation des composants
    initNavigation();
    initForms();
    initSmoothScroll();
    initResponsiveMenu();
    initServiceAccordions();
    initNewsletterSubscription();
});

// Navigation principale
function initNavigation() {
    const navLinks = document.querySelectorAll('[data-nav-link]');
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        // Marquer le lien actif
        if (link.pathname === currentPath) {
            link.classList.add('active');
        }

        // Gestion du clic
        link.addEventListener('click', function(e) {
            e.preventDefault();
            navigateTo(this.href);
        });
    });
}

function navigateTo(url) {
    // Ajouter ici une logique de transition de page si nécessaire
    window.location.href = url;
}

// Gestion des formulaires
function initForms() {
    document.querySelectorAll('[data-form]').forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formType = this.dataset.form;
            const formData = new FormData(this);
            const submitBtn = this.querySelector('[type="submit"]');

            try {
                submitBtn.disabled = true;
                
                // Exemple de traitement différencié
                switch(formType) {
                    case 'newsletter':
                        await handleNewsletter(formData);
                        break;
                    case 'service-request':
                        await handleServiceRequest(formData);
                        break;
                    default:
                        await handleGenericForm(formData);
                }

                showFormFeedback(this, 'success');
                this.reset();
            } catch (error) {
                showFormFeedback(this, 'error', error.message);
            } finally {
                submitBtn.disabled = false;
            }
        });
    });
}

// Scroll fluide
function initSmoothScroll() {
    document.querySelectorAll('[data-scroll]').forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.dataset.scroll);
            
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - config.scrollOffset,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Menu responsive
function initResponsiveMenu() {
    const menuToggle = document.createElement('button');
    menuToggle.innerHTML = '☰';
    menuToggle.className = 'mobile-menu-toggle';
    document.body.appendChild(menuToggle);

    const nav = document.querySelector('nav');
    
    menuToggle.addEventListener('click', () => {
        nav.classList.toggle('open');
        menuToggle.classList.toggle('active');
    });

    // Fermer le menu en cliquant à l'extérieur
    document.addEventListener('click', (e) => {
        if (!nav.contains(e.target) && !menuToggle.contains(e.target)) {
            nav.classList.remove('open');
            menuToggle.classList.remove('active');
        }
    });
}

// Services - Accordéon
function initServiceAccordions() {
    document.querySelectorAll('[data-accordion]').forEach(accordion => {
        const trigger = accordion.querySelector('[data-accordion-trigger]');
        const content = accordion.querySelector('[data-accordion-content]');

        trigger.addEventListener('click', () => {
            const isOpen = accordion.classList.toggle('active');
            content.style.maxHeight = isOpen ? `${content.scrollHeight}px` : '0';
        });
    });
}

// Newsletter
function initNewsletterSubscription() {
    const newsletterForm = document.querySelector('[data-form="newsletter"]');
    if (!newsletterForm) return;

    const emailInput = newsletterForm.querySelector('input[type="email"]');
    
    emailInput.addEventListener('input', () => {
        validateEmail(emailInput);
    });
}

// Helpers
async function handleNewsletter(formData) {
    // Exemple d'appel API
    const response = await fetch('/api/newsletter', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) throw new Error('Échec de l\'inscription');
    return response.json();
}

function validateEmail(input) {
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value);
    input.classList.toggle('is-invalid', !isValid);
    return isValid;
}

function showFormFeedback(form, type, message = '') {
    const feedback = form.querySelector('.form-feedback');
    if (!feedback) return;

    feedback.textContent = message || {
        success: 'Merci ! Votre demande a bien été envoyée.',
        error: 'Une erreur est survenue. Veuillez réessayer.'
    }[type];

    feedback.className = `form-feedback text-${type}`;
    feedback.hidden = false;

    setTimeout(() => {
        feedback.hidden = true;
    }, 5000);
}

// Styles dynamiques
const dynamicStyles = document.createElement('style');
dynamicStyles.textContent = `
    [data-accordion-content] {
        max-height: 0;
        overflow: hidden;
        transition: max-height ${config.animationDuration}ms ease;
    }

    .mobile-menu-toggle {
        display: none;
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        padding: 0.5rem;
        background: #fff;
        border: 1px solid #ddd;
    }

    @media (max-width: ${config.mobileBreakpoint}px) {
        .mobile-menu-toggle { display: block; }
        nav { display: none; }
        nav.open { display: block; }
    }

    .form-feedback {
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .form-feedback:not([hidden]) {
        opacity: 1;
    }
`;
document.head.appendChild(dynamicStyles);