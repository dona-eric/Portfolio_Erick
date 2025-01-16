document.addEventListener('DOMContentLoaded', function () {
    // Animation des cartes de projets lors du défilement
    const projectCards = document.querySelectorAll('.card');
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1,
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target); // Stop observing une fois visible
            }
        });
    }, observerOptions);

    projectCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = `translateY(${20 + index * 10}px)`; // Décalage varié
        card.style.transition = `all 0.5s ease-out ${index * 0.1}s`; // Délai croissant
        observer.observe(card);
    });

    // Animation du texte gradient
    const textGradient = document.querySelector('.text-gradient');
    if (textGradient) {
        textGradient.style.backgroundSize = '200% auto';
        textGradient.style.animation = 'gradient 3s linear infinite';
    }

    // Effets hover sur les boutons
    const projectButtons = document.querySelectorAll('.btn-outline-primary, .btn-outline-secondary');
    projectButtons.forEach(button => {
        button.addEventListener('mouseenter', function () {
            this.style.transform = 'scale(1.05)';
        });

        button.addEventListener('mouseleave', function () {
            this.style.transform = 'scale(1)';
        });
    });

    // Chargement des images
    const projectImages = document.querySelectorAll('.img-fluid');
    projectImages.forEach(img => {
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.5s ease';
        img.addEventListener('load', function () {
            this.style.opacity = '1';
        });
    });

    // Animation de la section Call to Action
    const ctaSection = document.querySelector('.bg-gradient-primary-to-secondary');
    if (ctaSection) {
        const ctaObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    ctaSection.style.transform = 'scale(1)';
                    ctaSection.style.opacity = '1';
                }
            });
        }, observerOptions);

        ctaSection.style.opacity = '0';
        ctaSection.style.transform = 'scale(0.95)';
        ctaSection.style.transition = 'all 0.5s ease';
        ctaObserver.observe(ctaSection);
    }
});

// Ajouter les styles CSS nécessaires
const style = document.createElement('style');
style.textContent = `
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    ..card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }

    .btn {
        transition: all 0.3s ease;
    }

    .text-gradient {
        background: linear-gradient(45deg, #007bff, #6610f2, #6f42c1);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        background
}