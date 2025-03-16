// contact.js
document.addEventListener('DOMContentLoaded', () => {
    class ContactForm {
        constructor() {
            this.form = document.getElementById('contactForm');
            this.submitButton = document.getElementById('submitButton');
            this.successMessage = document.getElementById('submitSuccessMessage');
            this.errorMessage = document.getElementById('submitErrorMessage');
            this.init();
        }

        init() {
            this.initEnvelopeAnimation();
            this.initFormValidation();
            this.initFormSubmission();
            this.injectStyles();
        }

        initEnvelopeAnimation() {
            const envelope = document.querySelector('.contact-envelope');
            if (!envelope) return;

            envelope.addEventListener('mouseenter', () => {
                envelope.style.transform = 'scale(1.2) rotate(15deg)';
            });

            envelope.addEventListener('mouseleave', () => {
                envelope.style.transform = 'scale(1) rotate(0)';
            });
        }

        initFormValidation() {
            this.inputs = this.form.querySelectorAll('[data-validation]');
            
            this.inputs.forEach(input => {
                input.addEventListener('input', this.validateField.bind(this, input));
                input.addEventListener('blur', this.validateField.bind(this, input));
            });
        }

        validateField(field) {
            const isValid = field.checkValidity();
            const feedback = field.parentElement.querySelector('.form-feedback');

            field.classList.toggle('is-invalid', !isValid);
            field.classList.toggle('is-valid', isValid);
            
            if (feedback) {
                feedback.textContent = field.validationMessage;
                feedback.hidden = isValid;
            }

            return isValid;
        }

        validateForm() {
            let isValid = true;
            this.inputs.forEach(input => {
                if (!this.validateField(input)) isValid = false;
            });
            return isValid;
        }

        async handleSubmit(e) {
            e.preventDefault();
            
            if (!this.validateForm()) return;

            const formData = new FormData(this.form);
            this.toggleLoadingState(true);

            try {
                // Remplacez par votre logique d'envoi réelle
                await this.sendFormData(formData);
                
                this.showFeedback('success');
                this.form.reset();
            } catch (error) {
                this.showFeedback('error');
                console.error('Erreur d\'envoi:', error);
            } finally {
                this.toggleLoadingState(false);
            }
        }

        async sendFormData(formData) {
            // Exemple avec fetch API
            const response = await fetch('https://api.example.com/contact', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Échec de l\'envoi');
            return response.json();
        }

        toggleLoadingState(isLoading) {
            this.submitButton.disabled = isLoading;
            this.submitButton.innerHTML = isLoading 
                ? '<span class="spinner-border spinner-border-sm" role="status"></span> Envoi...'
                : 'Envoyer le message';
        }

        showFeedback(type) {
            this.successMessage.hidden = type !== 'success';
            this.errorMessage.hidden = type !== 'error';
        }

        initFormSubmission() {
            this.form.addEventListener('submit', this.handleSubmit.bind(this));
        }

        injectStyles() {
            const styles = `
                .contact-envelope {
                    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }

                .form-feedback {
                    opacity: 0;
                    max-height: 0;
                    transition: all 0.3s ease;
                }

                .form-feedback:not([hidden]) {
                    opacity: 1;
                    max-height: 2rem;
                }

                .is-valid {
                    border-color: #28a745 !important;
                }

                .is-invalid {
                    border-color: #dc3545 !important;
                }

                @media (prefers-reduced-motion: reduce) {
                    .contact-envelope {
                        transition: none;
                    }
                }
            `;

            const styleSheet = document.createElement('style');
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        }
    }

    new ContactForm();
});

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
  
    // Validation de formulaire
    const form = document.querySelector('.contact-form');
    if (form) {
      form.addEventListener('submit', (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      });
    }
  });
  