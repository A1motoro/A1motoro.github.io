/**
 * Features Component
 * Dynamic feature cards with hover effects
 */

function FeaturesComponent(features = []) {
    const defaultFeatures = [
        {
            icon: "fas fa-blog",
            title: "Technical Blog",
            description: "Read my latest posts about programming, mathematics, and personal experiences. Discover tutorials, insights, and thoughts on various technical topics.",
            link: {
                text: "Explore Blog",
                href: "blogii/index.html"
            }
        },
        {
            icon: "fas fa-chart-line",
            title: "Data Analysis Tools",
            description: "Upload and analyze your CSV files with advanced statistical analysis, beautiful visualizations, and comprehensive data insights.",
            link: {
                text: "Try Analyzer",
                href: "data-analysis/csv-analyzer.html"
            }
        },
        {
            icon: "fas fa-user",
            title: "About Me",
            description: "Learn more about my journey as a developer, my interests, and the technologies I work with.",
            link: {
                text: "Learn More",
                href: "#about"
            }
        }
    ];

    const finalFeatures = features.length > 0 ? features : defaultFeatures;

    return {
        render: function(container) {
            const section = document.createElement('section');
            section.className = 'features-section';
            
            section.innerHTML = `
                <div class="monokai-container">
                    <h2 class="monokai-title monokai-center">What I Offer</h2>
                    <div class="features-grid">
                        ${finalFeatures.map(feature => `
                            <div class="feature-card" data-feature="${feature.title.toLowerCase().replace(/\s+/g, '-')}">
                                <div class="feature-icon">
                                    <i class="${feature.icon}"></i>
                                </div>
                                <h3 class="feature-title">${feature.title}</h3>
                                <p class="feature-description">${feature.description}</p>
                                <a href="${feature.link.href}" class="feature-link">
                                    ${feature.link.text} <i class="fas fa-arrow-right"></i>
                                </a>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            
            container.appendChild(section);
            this.setupHoverEffects();
            this.setupClickAnimations();
        },

        setupHoverEffects: function() {
            const cards = document.querySelectorAll('.feature-card');
            
            cards.forEach(card => {
                card.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-10px) scale(1.02)';
                    this.style.boxShadow = '0 15px 35px var(--monokai-shadow)';
                });
                
                card.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0) scale(1)';
                    this.style.boxShadow = '0 5px 15px var(--monokai-shadow)';
                });
            });
        },

        setupClickAnimations: function() {
            const links = document.querySelectorAll('.feature-link');
            
            links.forEach(link => {
                link.addEventListener('click', function(e) {
                    // Add click animation
                    this.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        this.style.transform = 'scale(1)';
                    }, 150);
                });
            });
        }
    };
}

