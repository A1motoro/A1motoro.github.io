/**
 * AIE Portfolio - JavaScript Framework Core
 * Dynamic content loading and component system
 * Author: A1m
 * Version: 1.0
 */

class AIEFramework {
    constructor() {
        this.components = new Map();
        this.themes = new Map();
        this.config = {
            lazyLoad: true,
            cacheComponents: true,
            animationDuration: 300
        };
        this.init();
    }

    init() {
        this.loadCoreStyles();
        this.setupEventListeners();
        this.loadComponents();
        console.log('🚀 AIE Framework initialized');
    }

    // Load core styles dynamically
    loadCoreStyles() {
        const styles = [
            'core-framework/themes/monokai-core.css',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
        ];

        styles.forEach(href => {
            if (!document.querySelector(`link[href="${href}"]`)) {
                const link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = href;
                document.head.appendChild(link);
            }
        });
    }

    // Setup global event listeners
    setupEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            this.initializePage();
        });

        // Smooth scrolling for anchor links
        document.addEventListener('click', (e) => {
            if (e.target.matches('a[href^="#"]')) {
                e.preventDefault();
                this.smoothScroll(e.target.getAttribute('href'));
            }
        });
    }

    // Initialize page-specific components
    initializePage() {
        const pageType = this.detectPageType();
        this.loadPageComponents(pageType);
        this.initializeAnimations();
    }

    // Detect current page type
    detectPageType() {
        const path = window.location.pathname;
        if (path.includes('blogii')) return 'blog';
        if (path.includes('data-analysis')) return 'analyzer';
        if (path.includes('portfolio')) return 'portfolio';
        if (path === '/' || path.endsWith('index.html')) return 'hub';
        return 'default';
    }

    // Load components based on page type
    loadPageComponents(pageType) {
        const componentMap = {
            'hub': ['navigation', 'hero', 'quick-links'],
            'portfolio': ['navigation', 'hero', 'features', 'about'],
            'blog': ['navigation', 'hero', 'posts', 'sidebar'],
            'analyzer': ['navigation', 'uploader', 'charts', 'analysis']
        };

        const components = componentMap[pageType] || ['navigation'];
        components.forEach(component => this.loadComponent(component));
    }

    // Load individual component
    async loadComponent(componentName) {
        if (this.components.has(componentName)) {
            return this.components.get(componentName);
        }

        try {
            const response = await fetch(`js-framework/components/${componentName}.js`);
            if (response.ok) {
                const componentCode = await response.text();
                const component = eval(`(${componentCode})`);
                this.components.set(componentName, component);
                return component;
            }
        } catch (error) {
            console.warn(`Component ${componentName} not found, using fallback`);
            return this.getFallbackComponent(componentName);
        }
    }

    // Fallback components for basic functionality
    getFallbackComponent(componentName) {
        const fallbacks = {
            'navigation': () => this.createNavigation(),
            'hero': () => this.createHero(),
            'quick-links': () => this.createQuickLinks()
        };
        return fallbacks[componentName] || (() => null);
    }

    // Create navigation component
    createNavigation() {
        return {
            render: (container) => {
                const nav = document.createElement('nav');
                nav.className = 'monokai-nav';
                nav.innerHTML = `
                    <div style="display: flex; align-items: center;">
                        <i class="fas fa-code" style="font-size: 25px; color: var(--monokai-accent); margin-right: 10px;"></i>
                        <a href="index.html" class="monokai-logo">AIE Portfolio</a>
                    </div>
                    <ul class="monokai-nav-links">
                        <li><a href="index.html">🏠 Hub</a></li>
                        <li><a href="portfolio.html">📋 Portfolio</a></li>
                        <li><a href="blogii/index.html">📝 Blog</a></li>
                        <li><a href="data-analysis/csv-analyzer.html">📊 Data Analysis</a></li>
                        <li><a href="#about">ℹ️ About</a></li>
                    </ul>
                `;
                container.appendChild(nav);
            }
        };
    }

    // Create hero section
    createHero() {
        return {
            render: (container) => {
                const hero = document.createElement('section');
                hero.className = 'hero-section';
                hero.innerHTML = `
                    <div class="hero-content">
                        <h1 class="hero-title">Welcome to AIE Portfolio</h1>
                        <p class="hero-subtitle">Developer & Data Analyst</p>
                        <p class="hero-description">
                            Explore my blog posts, data analysis tools, and development projects.
                        </p>
                        <div class="cta-buttons">
                            <a href="blogii/index.html" class="cta-button">
                                <i class="fas fa-blog"></i> Visit Blog
                            </a>
                            <a href="data-analysis/csv-analyzer.html" class="cta-button secondary">
                                <i class="fas fa-chart-line"></i> Analyze Data
                            </a>
                        </div>
                    </div>
                `;
                container.appendChild(hero);
            }
        };
    }

    // Create quick links
    createQuickLinks() {
        return {
            render: (container) => {
                const links = document.createElement('div');
                links.className = 'quick-links';
                links.innerHTML = `
                    <h3>Quick Access</h3>
                    <a href="portfolio.html">Portfolio Overview</a>
                    <a href="docs/README.md">Documentation</a>
                `;
                container.appendChild(links);
            }
        };
    }

    // Smooth scroll animation
    smoothScroll(target) {
        const element = document.querySelector(target);
        if (element) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }

    // Initialize animations
    initializeAnimations() {
        // Intersection Observer for scroll animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, { threshold: 0.1 });

        // Observe elements for animation
        document.querySelectorAll('.hero-section, .feature-card, .blog-card').forEach(el => {
            observer.observe(el);
        });
    }

    // Utility method to create elements with classes
    createElement(tag, className, content) {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (content) element.innerHTML = content;
        return element;
    }

    // Utility method to add event listeners
    addEventListeners(element, events) {
        Object.entries(events).forEach(([event, handler]) => {
            element.addEventListener(event, handler);
        });
    }
}

// Initialize framework when DOM is ready
const aieFramework = new AIEFramework();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIEFramework;
}
