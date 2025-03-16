document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitButton = form.querySelector('button[type="submit"]');
    const nameField = form.querySelector('#id_nom');
    const firstNameField = form.querySelector('#id_prenom');
    const emailField = form.querySelector('#id_email');
    const termsCheckbox = form.querySelector('#terms');

    // Fonction de validation pour chaque champ
    function validateForm() {
        let isValid = true;

        // Vérifier le champ Nom
        if (!nameField.value.trim()) {
            nameField.classList.add('is-invalid');
            isValid = false;
        } else {
            nameField.classList.remove('is-invalid');
        }

        // Vérifier le champ Prénom
        if (!firstNameField.value.trim()) {
            firstNameField.classList.add('is-invalid');
            isValid = false;
        } else {
            firstNameField.classList.remove('is-invalid');
        }

        // Vérifier l'email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailField.value.trim() || !emailRegex.test(emailField.value)) {
            emailField.classList.add('is-invalid');
            isValid = false;
        } else {
            emailField.classList.remove('is-invalid');
        }

        // Vérifier que l'utilisateur accepte les termes
        if (!termsCheckbox.checked) {
            termsCheckbox.classList.add('is-invalid');
            isValid = false;
        } else {
            termsCheckbox.classList.remove('is-invalid');
        }

        // Activer ou désactiver le bouton de soumission
        submitButton.disabled = !isValid;
    }

    // Écouter les événements sur les champs de saisie
    nameField.addEventListener('input', validateForm);
    firstNameField.addEventListener('input', validateForm);
    emailField.addEventListener('input', validateForm);
    termsCheckbox.addEventListener('change', validateForm);

    // Valider au chargement de la page pour la première fois
    validateForm();
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
});
