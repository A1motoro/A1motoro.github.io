/**
 * Hero Component
 * Dynamic hero sections with animations
 */

function HeroComponent(config = {}) {
    const defaultConfig = {
        title: "Welcome to AIE Portfolio",
        subtitle: "Developer & Data Analyst",
        description: "Explore my blog posts, data analysis tools, and development projects.",
        buttons: [
            {
                text: "Visit Blog",
                href: "blogii/index.html",
                icon: "fas fa-blog",
                class: "primary"
            },
            {
                text: "Analyze Data",
                href: "data-analysis/csv-analyzer.html",
                icon: "fas fa-chart-line",
                class: "secondary"
            }
        ],
        background: "gradient"
    };

    const finalConfig = { ...defaultConfig, ...config };

    return {
        render: function(container) {
            const hero = document.createElement('section');
            hero.className = `hero-section ${finalConfig.background}`;
            
            hero.innerHTML = `
                <div class="hero-content">
                    <h1 class="hero-title">${finalConfig.title}</h1>
                    <p class="hero-subtitle">${finalConfig.subtitle}</p>
                    <p class="hero-description">${finalConfig.description}</p>
                    <div class="cta-buttons">
                        ${finalConfig.buttons.map(btn => `
                            <a href="${btn.href}" class="cta-button ${btn.class}">
                                <i class="${btn.icon}"></i> ${btn.text}
                            </a>
                        `).join('')}
                    </div>
                </div>
            `;
            
            container.appendChild(hero);
            this.initializeAnimations();
        },

        initializeAnimations: function() {
            const hero = document.querySelector('.hero-section');
            if (hero) {
                // Add entrance animation
                hero.style.opacity = '0';
                hero.style.transform = 'translateY(30px)';
                
                setTimeout(() => {
                    hero.style.transition = 'all 0.8s ease-out';
                    hero.style.opacity = '1';
                    hero.style.transform = 'translateY(0)';
                }, 100);

                // Add floating animation to title
                const title = hero.querySelector('.hero-title');
                if (title) {
                    title.style.animation = 'monokaiFloat 3s ease-in-out infinite';
                }
            }
        }
    };
}

