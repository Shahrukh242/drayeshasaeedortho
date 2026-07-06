/* 
========================================================================
   DR. AYESHA SAEED PEDIATRIC ORTHOPEDICS - MAIN JAVASCRIPT
   Handles: Nav menus, scroll reveals, FAQ toggles, Testimonial sliders
========================================================================
*/

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. MOBILE NAV DRAWER TOGGLE
    const mobileNavToggle = document.getElementById('mobileNavToggle');
    const mobileNav = document.getElementById('mobileNav');
    const mobileNavOverlay = document.getElementById('mobileNavOverlay');

    if (mobileNavToggle && mobileNav && mobileNavOverlay) {
        const toggleMenu = () => {
            mobileNavToggle.classList.toggle('open');
            mobileNav.classList.toggle('open');
            mobileNavOverlay.classList.toggle('open');
            // Prevent body scroll when menu is open
            document.body.style.overflow = mobileNav.classList.contains('open') ? 'hidden' : '';
        };

        mobileNavToggle.addEventListener('click', toggleMenu);
        mobileNavOverlay.addEventListener('click', toggleMenu);

        // Close menu when clicking links
        const mobileLinks = mobileNav.querySelectorAll('.nav-link');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileNavToggle.classList.remove('open');
                mobileNav.classList.remove('open');
                mobileNavOverlay.classList.remove('open');
                document.body.style.overflow = '';
            });
        });
    }

    // 2. STICKY HEADER ON SCROLL
    const siteHeader = document.getElementById('siteHeader');
    if (siteHeader) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                siteHeader.classList.add('scrolled');
            } else {
                siteHeader.classList.remove('scrolled');
            }
        });
    }

    // 3. SCROLL REVEAL ANIMATIONS (INTERSECTION OBSERVER)
    const revealElements = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window && revealElements.length > 0) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    // Once animated, no need to track it anymore
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px' // Trigger slightly before element enters viewport
        });

        revealElements.forEach(el => revealObserver.observe(el));
    } else {
        // Fallback for older browsers
        revealElements.forEach(el => el.classList.add('active'));
    }

    // 4. FAQ ACCORDION LOGIC
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const questionButton = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');

        if (questionButton && answer) {
            questionButton.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                
                // Close all other FAQs first (Accordion behavior)
                faqItems.forEach(otherItem => {
                    otherItem.classList.remove('active');
                    otherItem.querySelector('.faq-answer').style.maxHeight = null;
                });

                if (!isActive) {
                    item.classList.add('active');
                    // Set height dynamically based on scrollHeight
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                }
            });
        }
    });

    // 5. TESTIMONIAL SLIDER/CAROUSEL CONTROL
    let currentSlide = 0;
    const slides = document.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('.slider-dot');
    let autoSlideInterval;

    window.setTestimonial = (index) => {
        if (slides.length === 0 || dots.length === 0) return;
        
        // Remove active states
        slides[currentSlide].classList.remove('active');
        dots[currentSlide].classList.remove('active');

        // Apply new active states
        currentSlide = index;
        slides[currentSlide].classList.add('active');
        dots[currentSlide].classList.add('active');

        // Reset auto interval
        resetAutoSlide();
    };

    const startAutoSlide = () => {
        if (slides.length <= 1) return;
        autoSlideInterval = setInterval(() => {
            let nextSlide = (currentSlide + 1) % slides.length;
            setTestimonial(nextSlide);
        }, 8000); // Shift every 8 seconds
    };

    const resetAutoSlide = () => {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    };

    if (slides.length > 0) {
        startAutoSlide();
    }
});
