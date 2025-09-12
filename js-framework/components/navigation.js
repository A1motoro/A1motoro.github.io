/**
 * Navigation Component
 * Dynamic navigation with responsive design
 */

function NavigationComponent() {
    return {
        render: function(container) {
            const nav = document.createElement('header');
            nav.className = 'monokai-header';
            
            nav.innerHTML = `
                <nav class="monokai-nav">
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
                    <div class="mobile-menu" style="display: none;">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </nav>
            `;
            
            container.appendChild(nav);
            this.setupMobileMenu();
            this.highlightActivePage();
        },

        setupMobileMenu: function() {
            const mobileMenu = document.querySelector('.mobile-menu');
            const navLinks = document.querySelector('.monokai-nav-links');
            
            if (mobileMenu && navLinks) {
                mobileMenu.addEventListener('click', function() {
                    navLinks.classList.toggle('active');
                });
            }
        },

        highlightActivePage: function() {
            const currentPage = window.location.pathname;
            const navLinks = document.querySelectorAll('.monokai-nav-links a');
            
            navLinks.forEach(link => {
                if (link.getAttribute('href') === currentPage || 
                    (currentPage.includes('blogii') && link.getAttribute('href').includes('blogii')) ||
                    (currentPage.includes('data-analysis') && link.getAttribute('href').includes('data-analysis'))) {
                    link.style.background = 'var(--monokai-bg-hover)';
                    link.style.color = 'var(--monokai-accent)';
                }
            });
        }
    };
}

