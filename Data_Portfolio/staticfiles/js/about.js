// about.js
document.addEventListener('DOMContentLoaded', () => {
    // Configuration des animations
    const animationConfig = {
        card: {
            transition: 'all 0.5s ease-out',
            initialTranslate: 'translateY(20px)',
            finalTranslate: 'translateY(0)'
        },
        skill: {
            hoverScale: 1.05,
            hoverShadow: '0 4px 8px rgba(0,0,0,0.1)'
        },
        date: {
            staggerDelay: 200,
            totalDelay: 500
        }
    };

    // Initialisation des composants
    initTextGradients();
    initCardsAnimation();
    initDownloadButton();
    initSkillsInteraction();
    initDatesAnimation();
    injectGlobalStyles();
});

function initTextGradients() {
    const gradients = document.querySelectorAll('.text-gradient');
    gradients.forEach(gradient => {
        gradient.style.backgroundSize = '200% auto';
        gradient.style.animation = 'text-gradient 3s linear infinite';
    });
}

function initCardsAnimation() {
    const observer = new IntersectionObserver(handleCardIntersection, {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    });

    document.querySelectorAll('.card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = animationConfig.card.initialTranslate;
        card.style.transition = animationConfig.card.transition;
        observer.observe(card);
    });
}

function handleCardIntersection(entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = animationConfig.card.finalTranslate;
            observer.unobserve(entry.target);
        }
    });
}

function initDownloadButton() {
    const btn = document.querySelector('.btn-download');
    if (!btn) return;

    const icon = btn.querySelector('.bi-download');
    
    btn.addEventListener('mouseenter', () => {
        btn.style.transform = 'translateY(-3px)';
        icon.style.transform = 'translateY(2px)';
    });

    btn.addEventListener('mouseleave', () => {
        btn.style.transform = 'translateY(0)';
        icon.style.transform = 'translateY(0)';
    });
}

function initSkillsInteraction() {
    document.querySelectorAll('.skill-item').forEach(item => {
        item.addEventListener('mouseenter', handleSkillHover);
        item.addEventListener('mouseleave', handleSkillLeave);
    });
}

function handleSkillHover(e) {
    const target = e.currentTarget;
    target.style.transform = `scale(${animationConfig.skill.hoverScale})`;
    target.style.boxShadow = animationConfig.skill.hoverShadow;
}

function handleSkillLeave(e) {
    const target = e.currentTarget;
    target.style.transform = 'scale(1)';
    target.style.boxShadow = 'none';
}

function initDatesAnimation() {
    const dates = document.querySelectorAll('.timeline-date');
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
            }, index * animationConfig.date.staggerDelay);
        });
    }, animationConfig.date.totalDelay);
}

function injectGlobalStyles() {
    const styles = `
        @keyframes text-gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .text-gradient {
            background: linear-gradient(45deg, #007bff, #6610f2, #6f42c1);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .skill-item {
            transition: all 0.3s ease;
            cursor: pointer;
            background: #f8f9fa;
            border-radius: 1rem;
        }

        .btn-download {
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .btn-download .bi-download {
            transition: transform 0.3s ease;
        }

        @media (prefers-reduced-motion: reduce) {
            * {
                transition: none !important;
                animation: none !important;
            }
        }
    `;

    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);
}