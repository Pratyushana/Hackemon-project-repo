// GRACE Voice Agent Website JavaScript - Enhanced Version

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation
    const mobileMenu = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');
    const navItems = document.querySelectorAll('.nav-links li');
    
    if (mobileMenu) {
        mobileMenu.addEventListener('click', () => {
            // Toggle Navigation
            navLinks.classList.toggle('nav-active');
            
            // Animate Links
            navItems.forEach((link, index) => {
                if (link.style.animation) {
                    link.style.animation = '';
                } else {
                    link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
                }
            });
            
            // Mobile Menu Animation
            mobileMenu.classList.toggle('toggle');
        });
    }
    
    // Scroll Animation
    const scrollElements = document.querySelectorAll('.scroll-animation');
    
    const elementInView = (el, dividend = 1) => {
        const elementTop = el.getBoundingClientRect().top;
        return (
            elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend
        );
    };
    
    const elementOutofView = (el) => {
        const elementTop = el.getBoundingClientRect().top;
        return (
            elementTop > (window.innerHeight || document.documentElement.clientHeight)
        );
    };
    
    const displayScrollElement = (element) => {
        element.classList.add('scrolled');
    };
    
    const hideScrollElement = (element) => {
        element.classList.remove('scrolled');
    };
    
    const handleScrollAnimation = () => {
        scrollElements.forEach((el) => {
            if (elementInView(el, 1.25)) {
                displayScrollElement(el);
            } else if (elementOutofView(el)) {
                hideScrollElement(el);
            }
        });
    };
    
    window.addEventListener('scroll', () => {
        handleScrollAnimation();
    });
    
    // Run once on load to check for elements already in view
    handleScrollAnimation();
    
    // Sticky Navigation
    const header = document.querySelector('header');
    const hero = document.querySelector('.hero');
    
    const stickyNav = (entries) => {
        const [entry] = entries;
        
        if (!entry.isIntersecting) {
            header.classList.add('sticky');
        } else {
            header.classList.remove('sticky');
        }
    };
    
    const heroObserver = new IntersectionObserver(stickyNav, {
        root: null,
        threshold: 0,
        rootMargin: '-80px'
    });
    
    if (hero) {
        heroObserver.observe(hero);
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (navLinks.classList.contains('nav-active')) {
                    mobileMenu.click();
                }
            }
        });
    });
    
    // Add animation classes to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.classList.add('scroll-animation');
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Contact Form Validation
    const contactForm = document.querySelector('.contact-form form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Simple validation
            let isValid = true;
            const formInputs = contactForm.querySelectorAll('input, textarea');
            
            formInputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                } else {
                    input.classList.remove('error');
                }
            });
            
            // Email validation
            const emailInput = contactForm.querySelector('input[type="email"]');
            if (emailInput && !validateEmail(emailInput.value)) {
                isValid = false;
                emailInput.classList.add('error');
            }
            
            if (isValid) {
                // Show success message (in real implementation, you would send data to server)
                const successMessage = document.createElement('div');
                successMessage.className = 'success-message';
                successMessage.innerHTML = '<i class="fas fa-check-circle"></i> Your message has been sent!';
                
                contactForm.innerHTML = '';
                contactForm.appendChild(successMessage);
            }
        });
        
        // Remove error class on input
        contactForm.querySelectorAll('input, textarea').forEach(input => {
            input.addEventListener('input', function() {
                if (this.value.trim()) {
                    this.classList.remove('error');
                }
            });
        });
    }
    
    // Helper function to validate email
    function validateEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }
    
    // Create a simple logo if none exists
    const logoImg = document.getElementById('logo-img');
    if (logoImg && logoImg.naturalWidth === 0) {
        createLogoPlaceholder(logoImg);
    }
    
    // Function to create a simple placeholder logo
    function createLogoPlaceholder(imgElement) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        canvas.width = 100;
        canvas.height = 100;
        
        // Create gradient background
        const gradient = ctx.createLinearGradient(0, 0, 100, 100);
        gradient.addColorStop(0, '#4e54c8');
        gradient.addColorStop(1, '#29dab5');
        
        // Draw circle
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(50, 50, 40, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw letter G
        ctx.fillStyle = 'white';
        ctx.font = 'bold 50px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('G', 50, 50);
        
        // Set canvas as image source
        imgElement.src = canvas.toDataURL();
    }
    
    // Add animated wave background to features section
    const features = document.querySelector('.features');
    if (features) {
        const wave = document.createElement('div');
        wave.className = 'wave-container';
        wave.innerHTML = `
            <div class="wave wave1"></div>
            <div class="wave wave2"></div>
            <div class="wave wave3"></div>
        `;
        features.prepend(wave);
    }
    
    // Add scroll-to-top button
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.className = 'scroll-top-btn';
    scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(scrollTopBtn);
    
    scrollTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Show/hide scroll-to-top button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollTopBtn.classList.add('show');
        } else {
            scrollTopBtn.classList.remove('show');
        }
    });
    
    // Add CSS for newly added elements
    const style = document.createElement('style');
    style.textContent = `
        .scroll-animation {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .scroll-animation.scrolled {
            opacity: 1;
            transform: translateY(0);
        }
        
        .toggle .line1 {
            transform: rotate(-45deg) translate(-5px, 6px);
        }
        
        .toggle .line2 {
            opacity: 0;
        }
        
        .toggle .line3 {
            transform: rotate(45deg) translate(-5px, -6px);
        }
        
        .sticky {
            background: rgba(255, 255, 255, 0.98);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .form-group input.error, .form-group textarea.error {
            border-color: #ff3860;
            box-shadow: 0 0 0 3px rgba(255, 56, 96, 0.1);
        }
        
        .success-message {
            text-align: center;
            color: #23d160;
            font-size: 1.2rem;
            padding: 40px 0;
        }
        
        .success-message i {
            font-size: 3rem;
            margin-bottom: 20px;
            display: block;
        }
        
        .wave-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
        }
        
        .wave {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 100px;
            background: url('data:image/svg+xml,<svg viewBox="0 0 1200 120" xmlns="http://www.w3.org/2000/svg"><path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" fill="rgba(255, 255, 255, 0.1)"></path></svg>');
            background-size: 1200px 100px;
        }
        
        .wave1 {
            animation: wave-animation 30s linear infinite;
            z-index: 1;
            opacity: 0.5;
            animation-delay: 0s;
            bottom: 0;
        }
        
        .wave2 {
            animation: wave-animation 15s linear infinite;
            z-index: 2;
            opacity: 0.3;
            animation-delay: -5s;
            bottom: 10px;
        }
        
        .wave3 {
            animation: wave-animation 20s linear infinite;
            z-index: 3;
            opacity: 0.2;
            animation-delay: -2s;
            bottom: 15px;
        }
        
        @keyframes wave-animation {
            0% {
                background-position-x: 0;
            }
            100% {
                background-position-x: 1200px;
            }
        }
        
        .scroll-top-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: var(--primary-color);
            color: white;
            border: none;
            cursor: pointer;
            font-size: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            visibility: hidden;
            transform: translateY(20px);
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(78, 84, 200, 0.3);
            z-index: 999;
        }
        
        .scroll-top-btn.show {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }
        
        .scroll-top-btn:hover {
            background: var(--accent-color);
            transform: translateY(-5px);
            box-shadow: 0 6px 20px rgba(78, 84, 200, 0.4);
        }
    `;
    document.head.appendChild(style);
    
    // Add particle background to hero section
    if (hero) {
        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'particles-container';
        hero.prepend(particlesContainer);
        
        // Create particles
        for (let i = 0; i < 20; i++) {
            createParticle(particlesContainer);
        }
    }
    
    // Function to create particles
    function createParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random size
        const size = Math.random() * 50 + 10;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // Random position
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        
        // Random opacity
        particle.style.opacity = Math.random() * 0.5 + 0.1;
        
        // Random animation delay
        particle.style.animationDelay = `${Math.random() * 5}s`;
        
        container.appendChild(particle);
    }
    
    // Add animated borders to sections
    const sections = document.querySelectorAll('.features, .tech, .demo, .download, .contact');
    sections.forEach(section => {
        const border = document.createElement('div');
        border.className = 'section-animated-border';
        
        const borderLine = document.createElement('div');
        borderLine.className = 'border-line';
        
        border.appendChild(borderLine);
        section.prepend(border);
    });
    
    // 3D tilt effect for cards
    const tiltElements = document.querySelectorAll('.feature-card, .tech-card, .contact-form');
    
    tiltElements.forEach(element => {
        element.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const angleX = (y - centerY) / 20;
            const angleY = (centerX - x) / 20;
            
            this.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) scale3d(1.02, 1.02, 1.02)`;
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
    
    // Add typing animation to hero subtitle
    const heroSubtitle = document.querySelector('.hero h2');
    if (heroSubtitle) {
        const text = heroSubtitle.textContent;
        heroSubtitle.textContent = '';
        
        let i = 0;
        function typeWriter() {
            if (i < text.length) {
                heroSubtitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        }
        
        // Start typing after a delay
        setTimeout(typeWriter, 1000);
    }
    
    // Enhance download button with pulse animation
    const downloadBtn = document.querySelector('.download-btn');
    if (downloadBtn) {
        downloadBtn.innerHTML += '<span class="pulse-effect"></span>';
        
        const style = document.createElement('style');
        style.textContent = `
            .download-btn {
                position: relative;
                overflow: hidden;
            }
            
            .pulse-effect {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.4);
                border-radius: var(--border-radius);
                animation: pulse 2s infinite;
                pointer-events: none;
            }
            
            @keyframes pulse {
                0% {
                    width: 0;
                    height: 0;
                    opacity: 0.5;
                }
                100% {
                    width: 200%;
                    height: 200%;
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Interactive command demonstration in the demo section
    const commandItems = document.querySelectorAll('.command-item');
    
    commandItems.forEach(item => {
        item.addEventListener('click', function() {
            const command = this.querySelector('.command').textContent;
            const description = this.querySelector('.description').textContent;
            
            // Create a demonstration element
            const demoElement = document.createElement('div');
            demoElement.className = 'command-demo';
            demoElement.innerHTML = `
                <div class="command-sim">
                    <div class="sim-input">
                        <span class="sim-prompt">User: </span>
                        <span class="sim-text">${command}</span>
                    </div>
                    <div class="sim-output">
                        <span class="sim-prompt">GRACE: </span>
                        <span class="sim-response">Processing command...</span>
                    </div>
                </div>
            `;
            
            // Add to demo container
            const demoContainer = document.querySelector('.demo-commands');
            
            // Remove any existing demo
            const existingDemo = document.querySelector('.command-demo');
            if (existingDemo) {
                existingDemo.remove();
            }
            
            demoContainer.appendChild(demoElement);
            
            // Simulate response
            setTimeout(() => {
                const response = demoElement.querySelector('.sim-response');
                response.textContent = `Executing: ${description.toLowerCase()}`;
                
                // Add completion message after execution
                setTimeout(() => {
                    const completionDiv = document.createElement('div');
                    completionDiv.className = 'sim-completion';
                    completionDiv.innerHTML = '<i class="fas fa-check-circle"></i> Command completed successfully!';
                    demoElement.querySelector('.command-sim').appendChild(completionDiv);
                }, 1500);
            }, 800);
            
            // Add styles for the simulation
            const style = document.createElement('style');
            style.textContent = `
                .command-demo {
                    margin-top: 20px;
                    padding: 15px;
                    background: #2d2d2d;
                    border-radius: 8px;
                    color: #fff;
                    font-family: monospace;
                    animation: fadeIn 0.5s ease-in-out;
                }
                
                .command-sim {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }
                
                .sim-input, .sim-output {
                    line-height: 1.5;
                }
                
                .sim-prompt {
                    color: #29dab5;
                    font-weight: bold;
                }
                
                .sim-text {
                    color: #fff;
                }
                
                .sim-response {
                    color: #8f94fb;
                }
                
                .sim-completion {
                    margin-top: 10px;
                    color: #29dab5;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    font-size: 0.9em;
                    animation: fadeIn 0.5s ease-in-out;
                }
                
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            `;
            document.head.appendChild(style);
        });
    });

    // Add scroll-triggered animations to sections
    const animateSections = document.querySelectorAll('section');
    
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px'
    };
    
    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('section-visible');
                
                // Animate title separately
                const title = entry.target.querySelector('.section-title');
                if (title) {
                    title.classList.add('title-visible');
                }
                
                // Animation for content based on section
                if (entry.target.classList.contains('features')) {
                    const featureCards = entry.target.querySelectorAll('.feature-card');
                    featureCards.forEach((card, index) => {
                        setTimeout(() => {
                            card.classList.add('card-visible');
                        }, index * 100);
                    });
                }
                
                if (entry.target.classList.contains('tech')) {
                    const techCards = entry.target.querySelectorAll('.tech-card');
                    techCards.forEach((card, index) => {
                        setTimeout(() => {
                            card.classList.add('card-visible');
                        }, index * 150);
                    });
                }
            }
        });
    }, observerOptions);
    
    animateSections.forEach(section => {
        sectionObserver.observe(section);
    });
    
    // Add styles for section animations
    const sectionAnimStyles = document.createElement('style');
    sectionAnimStyles.textContent = `
        section {
            opacity: 0.8;
            transform: translateY(20px);
            transition: opacity 0.8s ease, transform 0.8s ease;
        }
        
        .section-visible {
            opacity: 1;
            transform: translateY(0);
        }
        
        .section-title {
            opacity: 0.5;
            transform: translateY(15px);
            transition: opacity 0.8s ease 0.2s, transform 0.8s ease 0.2s;
        }
        
        .title-visible {
            opacity: 1;
            transform: translateY(0);
        }
        
        .feature-card, .tech-card {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.5s ease, transform 0.5s ease;
        }
        
        .card-visible {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(sectionAnimStyles);
}); 