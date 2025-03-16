// articles.js
document.addEventListener('DOMContentLoaded', () => {
    const animationConfig = {
        textGradient: {
            animation: 'text-gradient 3s linear infinite'
        },
        card: {
            translateY: '20px',
            transition: 'all 0.3s ease',
            hoverTranslate: '-5px'
        },
        link: {
            hoverTranslate: '10px',
            transition: 'all 0.3s ease'
        },
        image: {
            loadTransition: 'opacity 0.5s ease',
            hoverScale: 1.05
        }
    };

    initTextGradient(animationConfig.textGradient);
    initArticleCards(animationConfig.card);
    initArticleLinks(animationConfig.link);
    initArticleImages(animationConfig.image);
    injectArticleStyles();
});

function initTextGradient(config) {
    const gradients = document.querySelectorAll('.article-title-gradient');
    gradients.forEach(gradient => {
        gradient.style.backgroundSize = '200% auto';
        gradient.style.animation = config.animation;
    });
}

function initArticleCards(config) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCard(entry.target, '0', 'translateY(0)');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.article-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = `translateY(${config.translateY})`;
        card.style.transition = config.transition;
        
        card.addEventListener('mouseenter', () => 
            handleCardHover(card, config.hoverTranslate));
        card.addEventListener('mouseleave', () => 
            handleCardHover(card, '0'));
        
        observer.observe(card);
    });
}

function animateCard(element, opacity, transform) {
    element.style.opacity = opacity;
    element.style.transform = transform;
}

function handleCardHover(card, translate) {
    if (window.matchMedia('(hover: hover)').matches) {
        card.style.transform = `translateY(${translate})`;
    }
}

function initArticleLinks(config) {
    document.querySelectorAll('.article-link').forEach(link => {
        link.style.transition = config.transition;
        
        link.addEventListener('mouseenter', () => 
            handleLinkHover(link, config.hoverTranslate));
        link.addEventListener('mouseleave', () => 
            handleLinkHover(link, '0'));
    });
}

function handleLinkHover(link, translate) {
    if (window.matchMedia('(hover: hover)').matches) {
        link.style.transform = `translateX(${translate})`;
    }
}

function initArticleImages(config) {
    document.querySelectorAll('.article-image').forEach(img => {
        img.style.opacity = '0';
        img.style.transition = config.loadTransition;
        
        img.addEventListener('load', () => {
            img.style.opacity = '1';
            img.style.transform = 'scale(1)';
        });
        
        img.addEventListener('mouseenter', () => 
            img.style.transform = `scale(${config.hoverScale})`);
        img.addEventListener('mouseleave', () => 
            img.style.transform = 'scale(1)');
    });
}

function injectArticleStyles() {
    const styles = `
        @keyframes text-gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .article-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            will-change: transform;
        }

        .article-link {
            display: inline-block;
            color: #007bff;
            text-decoration: none;
            position: relative;
            backface-visibility: hidden;
        }

        .article-link::after {
            content: '';
            position: absolute;
            width: 100%;
            height: 2px;
            bottom: 0;
            left: 0;
            background-color: currentColor;
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .article-link:hover::after {
            transform: scaleX(1);
        }

        .article-image {
            border-radius: 0.5rem;
            transform: translateZ(0);
        }

        @media (prefers-reduced-motion: reduce) {
            .article-card,
            .article-link,
            .article-image {
                transition: none !important;
                animation: none !important;
            }
        }
    `;

    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);
}