document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const submitButton = document.getElementById('submitButton');
    const successMessage = document.getElementById('submitSuccessMessage');
    const errorMessage = document.getElementById('submitErrorMessage');

    // Animation de l'icône d'enveloppe
    const envelopeIcon = document.querySelector('.bi-envelope');
    if (envelopeIcon) {
        envelopeIcon.parentElement.addEventListener('mouseenter', function() {
            envelopeIcon.style.transform = 'scale(1.2) rotate(15deg)';
        });
        
        envelopeIcon.parentElement.addEventListener('mouseleave', function() {
            envelopeIcon.style.transform = 'scale(1) rotate(0)';
        });
    }

    // Fonction de validation d'email
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // Fonction de validation de numéro de téléphone
    function isValidPhone(phone) {
        return /^[\d\s()-+]{8,}$/.test(phone);
    }

    // Gérer la validation en temps réel des champs
    const inputs = form.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateField(this);
            checkFormValidity();
        });

        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            validateField(this);
        });
    });

    // Valider un champ spécifique
    function validateField(field) {
        const feedback = field.parentElement.querySelector('.invalid-feedback');
        let isValid = true;

        if (field.hasAttribute('data-sb-validations')) {
            const validations = field.getAttribute('data-sb-validations').split(',');

            if (validations.includes('required') && !field.value.trim()) {
                isValid = false;
            }

            if (field.type === 'email' && validations.includes('email') && !isValidEmail(field.value)) {
                isValid = false;
            }

            if (field.type === 'tel' && !isValidPhone(field.value)) {
                isValid = false;
            }
        }

        if (!isValid) {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
            if (feedback) feedback.style.display = 'block';
        } else {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
            if (feedback) feedback.style.display = 'none';
        }

        return isValid;
    }

    // Vérifier la validité du formulaire complet
    function checkFormValidity() {
        let isValid = true;
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });

        if (isValid) {
            submitButton.classList.remove('disabled');
        } else {
            submitButton.classList.add('disabled');
        }
    }

    // Gérer la soumission du formulaire
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            // Simulation d'envoi (à remplacer par votre logique d'envoi réelle)
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            successMessage.classList.remove('d-none');
            errorMessage.classList.add('d-none');
            form.reset();
            inputs.forEach(input => {
                input.classList.remove('is-valid');
            });
            submitButton.classList.add('disabled');
        } catch (error) {
            errorMessage.classList.remove('d-none');
            successMessage.classList.add('d-none');
        }


        alert('Merci d\'avoir rempli le formulaire ! Nous vous contacterons bientôt.');
        // form.reset(); // Réinitialise le formulaire après soumission
    });
});

document.head.appendChild(style);


// contacts.js
const formObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.classList.add('in-view');
        }
    });
});

// Observer pour le formulaire
const form = document.querySelector('.contact-form');
formObserver.observe(form);

// Observers pour les groupes de formulaire
document.querySelectorAll('.form-group').forEach((group, index) => {
    group.style.transitionDelay = `${index * 0.1}s`;
    formObserver.observe(group);
});

// Animation au focus
document.querySelectorAll('.form-input').forEach(input => {
    input.addEventListener('focus', () => {
        input.parentElement.querySelector('.form-label').style.transform = 'translateY(0)';
        input.parentElement.querySelector('.form-label').style.opacity = '1';
    });
});
