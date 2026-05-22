/**
 * Tatle tale Website Polish & Interactions
 */
document.addEventListener('DOMContentLoaded', function() {
    initScrollReveal();
    initMobileMenuFix();
    fixNavbarLinks();
});

/**
 * Reveal elements as they scroll into view
 */
function initScrollReveal() {
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('tt-visible');
                // Once revealed, no need to observe anymore
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Auto-reveal sections and images
    const elementsToReveal = document.querySelectorAll('section, .wixui-section, .wixui-image, .wow-image, .tt-workshop-card');
    elementsToReveal.forEach(el => {
        el.setAttribute('data-tt-reveal', '');
        observer.observe(el);
    });
}

/**
 * Ensure mobile menu works correctly and closes on link click
 */
function initMobileMenuFix() {
    const overlay = document.getElementById('tt-mobile-menu-overlay');
    if (!overlay) return;

    const navLinks = overlay.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            overlay.classList.remove('open');
            document.body.style.overflow = '';
        });
    });
}

/**
 * Surgical fix for navbar links if they are still using Wix format
 */
function fixNavbarLinks() {
    const links = document.querySelectorAll('a[data-testid="linkElement"], .wixui-horizontal-menu__item-link');
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (!href) return;

        // Clean up Wix URLs
        if (href.includes('turtle-tales-story')) link.setAttribute('href', '/turtle-tales-story');
        if (href.includes('workshop-chapters')) link.setAttribute('href', '/workshop-chapters');
        if (href.includes('community-survey')) link.setAttribute('href', '/community-survey');
        if (href.includes('about-lana')) link.setAttribute('href', '/about-lana');
        if (href === '/index.html' || href === 'index.html') link.setAttribute('href', '/');
    });
}
