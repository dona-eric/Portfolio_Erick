document.addEventListener('DOMContentLoaded', function () {
    // Ajouter les styles CSS dynamiquement
    addCustomStyles();

    // Initialiser les animations
    initTitleAnimation();
    initCardAnimations();
    initButtonHoverEffect();
    initSkillHoverEffect();
    initDateProgressionAnimation();
});

/**
 * Ajoute les styles CSS nécessaires dynamiquement.
 */
function addCustomStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .text-gradient {
            background: linear-gradient(45deg, #007bff, #6610f2, #6f42c1);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            background-size: 200% auto;
        }

        .card {
            transition: all 0.3s ease;
        }

        .btn-primary {
            transition: all 0.3s ease;
        }

        .bg-light.rounded-4 {
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .bi-download {
            transition: transform 0.3s ease;
        }

        .feature {
            transition: transform 0.3s ease;
        }

        .feature:hover {
            transform: rotate(15deg);
        }
    `;
    document.head.appendChild(style);
}

/**
 * Initialise l'animation du titre principal.
 */
function initTitleAnimation() {
    const textGradients = document.querySelectorAll('.text-gradient');
    textGradients.forEach(text => {
        text.style.backgroundSize = '200% auto';
        text.style.animation = 'gradient 3s linear infinite';
    });
}

/**
 * Initialise les animations pour les cartes d'expérience et d'éducation.
 */
function initCardAnimations() {
    const cards = document.querySelectorAll('.card');

    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.5s ease-out';
        observer.observe(card);
    });
}

/**
 * Initialise l'effet de survol pour le bouton de téléchargement.
 */
function initButtonHoverEffect() {
    const downloadBtn = document.querySelector('.btn-primary');
    if (downloadBtn) {
        downloadBtn.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-3px)';
            const icon = this.querySelector('.bi-download');
            if (icon) icon.style.transform = 'translateY(2px)';
        });

        downloadBtn.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
            const icon = this.querySelector('.bi-download');
            if (icon) icon.style.transform = 'translateY(0)';
        });
    }
}

/**
 * Initialise les effets de survol pour les compétences.
 */
function initSkillHoverEffect() {
    const skillItems = document.querySelectorAll('.bg-light.rounded-4');
    skillItems.forEach(item => {
        item.addEventListener('mouseenter', function () {
            this.style.transform = 'scale(1.05)';
            this.style.backgroundColor = '#f8f9fa';
            this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
        });

        item.addEventListener('mouseleave', function () {
            this.style.transform = 'scale(1)';
            this.style.backgroundColor = '#f8f9fa';
            this.style.boxShadow = 'none';
        });
    });
}

/**
 * Initialise l'animation de progression pour les dates.
 */
function initDateProgressionAnimation() {
    const dates = document.querySelectorAll('.text-primary.fw-bolder, .text-secondary.fw-bolder');
    dates.forEach(date => {
        date.style.opacity = '0';
        date.style.transform = 'translateX(-20px)';
        date.style.transition = 'all 0.5s ease';
    });

    setTimeout(() => {
        dates.forEach((date, index) => {
            setTimeout(() => {
                date.style.opacity = '1';
                date.style.transform = 'translateX(0)';
            }, index * 200);
        });
    }, 500);
}
