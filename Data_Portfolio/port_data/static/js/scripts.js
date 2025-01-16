document.addEventListener('DOMContentLoaded', function () {
    // Gère l'état "actif" pour les liens du menu
    const menuLinks = document.querySelectorAll('nav a');
    menuLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            // Supprime la classe "active" de tous les liens
            menuLinks.forEach(l => l.classList.remove('active'));
            // Ajoute la classe "active" au lien cliqué
            this.classList.add('active');
        });
    });

    // Gestion des formulaires (prévention par défaut + exemple d'alerte)
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            // Exemple de message (remplacez par votre propre logique)
            alert('Formulaire soumis !');
        });
    });

    // Gestion du défilement fluide pour les boutons "En savoir plus"
    const learnMoreButtons = document.querySelectorAll('.btn-learn-more');
    learnMoreButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Emp
