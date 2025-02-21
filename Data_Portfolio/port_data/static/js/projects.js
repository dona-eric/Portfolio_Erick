// projects.js

function handleButtonHover(button, scale) {
    if (window.matchMedia('(hover: hover)').matches) {
        button.style.transform = `scale(${scale})`;
    }
}
document.addEventListener('DOMContentLoaded', () => {
    const animationConfig = {
        card: {
            translateY: '50px',
            transition: 'all 0.5s ease-out',
            observerThreshold: 0.1
        },
        button: {
            hoverScale: 1.05,
            transition: 'transform 0.2s ease'
        },
        image: {
            loadTransition: 'opacity 0.5s ease'
        },
        cta: {
            scale: 0.95,
            transition: 'all 0.5s ease'
        }
    };

    initProjectCards(animationConfig.card);
    initTextGradient();
    initProjectButtons(animationConfig.button);
    initImageLoading(animationConfig.image);
    initCTASection(animationConfig.cta);
    injectProjectStyles();
});

function initProjectCards(config) {
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCardIn(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        rootMargin: '0px',
        threshold: config.observerThreshold
    });

    document.querySelectorAll('.project-card').forEach(card => {
        resetCardStyle(card, config);
        observer.observe(card);
    });
}

function resetCardStyle(card, config) {
    card.style.opacity = '0';
    card.style.transform = `translateY(${config.translateY})`;
    card.style.transition = config.transition;
}

function animateCardIn(card) {
    card.style.opacity = '1';
    card.style.transform = 'translateY(0)';
}

function initTextGradient() {
    const gradientElements = document.querySelectorAll('.text-gradient');
    gradientElements.forEach(el => {
        el.style.backgroundSize = '200% auto';
        el.style.animation = 'text-gradient 3s linear infinite';
    });
}

function initProjectButtons(config) {
    document.querySelectorAll('.project-button').forEach(button => {
        button.addEventListener('mouseenter', () => 
            handleButtonHover(button, config.hoverScale));
        button.addEventListener('mouseleave', handleButtonLeave);
        button.style.transition = config.transition;
    });
}

function handleButtonHover(button, scale) {
    button.style.transform = `scale(${scale})`;
}

function handleButtonLeave(e) {
    e.currentTarget.style.transform = 'scale(1)';
}

function initImageLoading(config) {
    document.querySelectorAll('.project-image').forEach(img => {
        img.style.opacity = '0';
        img.style.transition = config.loadTransition;
        img.addEventListener('load', () => img.style.opacity = '1');
    });
}

function initCTASection(config) {
    const cta = document.querySelector('.project-cta');
    if (!cta) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) animateCTASection(entry.target);
        });
    });

    cta.style.opacity = '0';
    cta.style.transform = `scale(${config.scale})`;
    cta.style.transition = config.transition;
    observer.observe(cta);
}

function animateCTASection(cta) {
    cta.style.opacity = '1';
    cta.style.transform = 'scale(1)';
}

function injectProjectStyles() {
    const styles = `
        @keyframes text-gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .project-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            will-change: transform;
        }

        .project-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        .project-button {
            transition: all 0.3s ease;
            backface-visibility: hidden;
        }

        .text-gradient {
            background: linear-gradient(45deg, #007bff, #6610f2, #6f42c1);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        @media (prefers-reduced-motion: reduce) {
            .project-card,
            .project-button {
                transition: none !important;
                animation: none !important;
            }
        }
    `;

    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);
}