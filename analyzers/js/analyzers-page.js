// Enhanced Analyzers Page JavaScript - Performance Optimized
class AnalyzersPage {
    constructor() {
        this.analyzers = [];
        this.filteredAnalyzers = [];
        this.searchTerm = '';
        this.currentFilter = 'all';
        this.isLoading = false;
        this.animationFrameId = null;
        this.debounceTimer = null;
        this.observer = null;
        
        // Performance optimizations
        this.cache = new Map();
        this.throttledFunctions = new Map();
        
        this.init();
    }

    async init() {
        try {
            // Load core components in parallel
            await this.loadCoreComponents();
            
            // Initialize data
            this.initializeAnalyzers();
            
            // Setup all functionality
            this.setupEventListeners();
            this.setupAnimations();
            this.setupSearch();
            this.setupFiltering();
            this.setupTooltips();
            this.setupKeyboardNavigation();
            this.setupPerformanceOptimizations();
            
            // Initial render
            this.renderAnalyzers();
            
            console.log('AnalyzersPage initialized successfully');
        } catch (error) {
            console.error('Error initializing AnalyzersPage:', error);
        }
    }

    async loadCoreComponents() {
        const startTime = performance.now();
        
        try {
            const [navResponse, footerResponse] = await Promise.all([
                fetch('../core-framework/components/navigation.html', { 
                    cache: 'force-cache',
                    headers: { 'Cache-Control': 'max-age=3600' }
                }),
                fetch('../core-framework/components/footer.html', { 
                    cache: 'force-cache',
                    headers: { 'Cache-Control': 'max-age=3600' }
                })
            ]);
            
            if (!navResponse.ok || !footerResponse.ok) {
                throw new Error('Failed to load components');
            }
            
            const [navData, footerData] = await Promise.all([
                navResponse.text(),
                footerResponse.text()
            ]);
            
            // Use requestAnimationFrame for smooth DOM updates
            this.raf(() => {
                document.getElementById('navigation-placeholder').innerHTML = navData;
                document.getElementById('footer-placeholder').innerHTML = footerData;
            });
            
            const loadTime = performance.now() - startTime;
            console.log(`Core components loaded in ${loadTime.toFixed(2)}ms`);
            
        } catch (error) {
            console.error('Error loading core components:', error);
            // Fallback content
            document.getElementById('navigation-placeholder').innerHTML = '<nav>Navigation unavailable</nav>';
            document.getElementById('footer-placeholder').innerHTML = '<footer>Footer unavailable</footer>';
        }
    }

    initializeAnalyzers() {
        this.analyzers = [
            {
                id: 'csv',
                title: 'CSV Analyzer',
                description: 'Upload and analyze CSV files with comprehensive statistical analysis, data visualization, and export capabilities.',
                icon: 'fas fa-file-csv',
                features: ['Statistical analysis and summaries', 'Interactive data visualization', 'Data cleaning and preprocessing', 'Export results in multiple formats'],
                link: 'csv-analyzer.html',
                status: 'available',
                category: 'data',
                popularity: 95,
                lastUpdated: '2024-01-15',
                tags: ['csv', 'data', 'analysis', 'statistics', 'visualization']
            },
            {
                id: 'json',
                title: 'JSON Analyzer',
                description: 'Analyze JSON data structures, validate schemas, and visualize hierarchical data relationships.',
                icon: 'fas fa-file-code',
                features: ['JSON schema validation', 'Tree structure visualization', 'Data type analysis', 'Format conversion tools'],
                link: '#',
                status: 'coming-soon',
                category: 'data',
                popularity: 78,
                lastUpdated: '2024-02-01',
                tags: ['json', 'data', 'validation', 'tree', 'structure']
            },
            {
                id: 'xml',
                title: 'XML Analyzer',
                description: 'Process and analyze XML documents with XPath queries, schema validation, and data extraction tools.',
                icon: 'fas fa-file-alt',
                features: ['XPath query builder', 'XML schema validation', 'Data extraction tools', 'Format transformation'],
                link: '#',
                status: 'coming-soon',
                category: 'data',
                popularity: 65,
                lastUpdated: '2024-02-15',
                tags: ['xml', 'data', 'xpath', 'validation', 'extraction']
            },
            {
                id: 'database',
                title: 'Database Analyzer',
                description: 'Connect to databases and perform advanced queries, relationship analysis, and performance monitoring.',
                icon: 'fas fa-database',
                features: ['Multi-database support', 'Query optimization', 'Relationship mapping', 'Performance metrics'],
                link: '#',
                status: 'coming-soon',
                category: 'database',
                popularity: 88,
                lastUpdated: '2024-03-01',
                tags: ['database', 'sql', 'queries', 'performance', 'relationships']
            },
            {
                id: 'text',
                title: 'Text Analyzer',
                description: 'Analyze text data with natural language processing, sentiment analysis, and keyword extraction.',
                icon: 'fas fa-font',
                features: ['Sentiment analysis', 'Keyword extraction', 'Text statistics', 'Language detection'],
                link: '#',
                status: 'coming-soon',
                category: 'nlp',
                popularity: 72,
                lastUpdated: '2024-03-15',
                tags: ['text', 'nlp', 'sentiment', 'keywords', 'language']
            },
            {
                id: 'image',
                title: 'Image Analyzer',
                description: 'Analyze image metadata, perform basic image processing, and extract visual information.',
                icon: 'fas fa-image',
                features: ['Metadata extraction', 'Color analysis', 'Basic image processing', 'Format conversion'],
                link: '#',
                status: 'coming-soon',
                category: 'media',
                popularity: 58,
                lastUpdated: '2024-04-01',
                tags: ['image', 'metadata', 'processing', 'color', 'visual']
            }
        ];
        
        this.filteredAnalyzers = [...this.analyzers];
    }

    setupEventListeners() {
        // Use event delegation for better performance
        document.addEventListener('click', this.handleClick.bind(this));
        document.addEventListener('keydown', this.handleKeyboard.bind(this));
        window.addEventListener('resize', this.throttle(this.handleResize.bind(this), 100));
        window.addEventListener('scroll', this.throttle(this.handleScroll.bind(this), 16));
    }

    setupAnimations() {
        // Use Intersection Observer for efficient scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    // Unobserve after animation to improve performance
                    this.observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Add CSS animations
        this.addAnimationStyles();
    }

    addAnimationStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .analyzer-card {
                opacity: 0;
                transform: translateY(30px);
                transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
                will-change: transform, opacity;
            }
            
            .analyzer-card.animate-in {
                opacity: 1;
                transform: translateY(0);
            }
            
            .analyzer-card:hover {
                transform: translateY(-5px) scale(1.02);
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .analyzer-icon {
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                will-change: transform;
            }
            
            .analyzer-card:hover .analyzer-icon {
                transform: scale(1.1) rotate(5deg);
            }
            
            .search-box input:focus {
                transform: scale(1.02);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .filter-btn {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                will-change: transform, background-color;
            }
            
            .filter-btn:hover {
                transform: translateY(-2px);
            }
        `;
        document.head.appendChild(style);
    }

    setupSearch() {
        // Create search interface
        const searchContainer = this.createElement('div', 'search-container');
        searchContainer.innerHTML = `
            <div class="search-box">
                <i class="fas fa-search search-icon"></i>
                <input type="text" id="analyzer-search" placeholder="Search analyzers..." autocomplete="off" spellcheck="false">
                <button class="clear-search" id="clear-search" style="display: none;" aria-label="Clear search">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="search-suggestions" id="search-suggestions" style="display: none;"></div>
        `;

        // Insert before grid
        const grid = document.querySelector('.analyzers-grid');
        grid.parentNode.insertBefore(searchContainer, grid);

        // Add search styles
        this.addSearchStyles();

        // Setup search functionality with debouncing
        const searchInput = document.getElementById('analyzer-search');
        const clearButton = document.getElementById('clear-search');
        const suggestions = document.getElementById('search-suggestions');

        // Debounced search function
        const debouncedSearch = this.debounce((value) => {
            this.searchTerm = value.toLowerCase();
            this.filterAnalyzers();
            this.updateSearchUI();
        }, 300);

        searchInput.addEventListener('input', (e) => {
            const value = e.target.value;
            debouncedSearch(value);
            
            if (value.length > 0) {
                this.showSuggestions(value);
            } else {
                this.hideSuggestions();
            }
        });

        searchInput.addEventListener('focus', () => {
            if (this.searchTerm) {
                this.showSuggestions(this.searchTerm);
            }
        });

        clearButton.addEventListener('click', () => {
            searchInput.value = '';
            this.searchTerm = '';
            this.filterAnalyzers();
            this.hideSuggestions();
            searchInput.focus();
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!searchContainer.contains(e.target)) {
                this.hideSuggestions();
            }
        });
    }

    addSearchStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .search-container {
                margin: 2rem 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                position: relative;
            }
            
            .search-box {
                position: relative;
                max-width: 400px;
                width: 100%;
            }
            
            .search-box input {
                width: 100%;
                padding: 1rem 3rem 1rem 3rem;
                border: 2px solid var(--monokai-border);
                border-radius: 25px;
                background: var(--monokai-bg);
                color: var(--monokai-fg);
                font-size: 1rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-sizing: border-box;
            }
            
            .search-box input:focus {
                outline: none;
                border-color: var(--monokai-accent);
                box-shadow: 0 0 20px var(--monokai-glow);
            }
            
            .search-icon {
                position: absolute;
                left: 1rem;
                top: 50%;
                transform: translateY(-50%);
                color: var(--monokai-comment);
                pointer-events: none;
            }
            
            .clear-search {
                position: absolute;
                right: 1rem;
                top: 50%;
                transform: translateY(-50%);
                background: none;
                border: none;
                color: var(--monokai-comment);
                cursor: pointer;
                padding: 0.5rem;
                border-radius: 50%;
                transition: all 0.3s ease;
            }
            
            .clear-search:hover {
                background: var(--monokai-bg-light);
                color: var(--monokai-accent);
            }
            
            .search-suggestions {
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: var(--monokai-bg);
                border: 1px solid var(--monokai-border);
                border-radius: 0 0 15px 15px;
                max-height: 200px;
                overflow-y: auto;
                z-index: 1000;
                box-shadow: 0 5px 15px var(--monokai-shadow);
            }
            
            .suggestion-item {
                padding: 0.75rem 1rem;
                cursor: pointer;
                border-bottom: 1px solid var(--monokai-border);
                transition: background-color 0.2s ease;
            }
            
            .suggestion-item:hover {
                background: var(--monokai-bg-light);
            }
            
            .suggestion-item:last-child {
                border-bottom: none;
            }
        `;
        document.head.appendChild(style);
    }

    setupFiltering() {
        // Create filter interface
        const filterContainer = this.createElement('div', 'filter-container');
        filterContainer.innerHTML = `
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="data">Data</button>
                <button class="filter-btn" data-filter="database">Database</button>
                <button class="filter-btn" data-filter="nlp">NLP</button>
                <button class="filter-btn" data-filter="media">Media</button>
                <button class="filter-btn" data-filter="available">Available</button>
            </div>
            <div class="filter-stats" id="filter-stats"></div>
        `;

        // Insert before grid
        const grid = document.querySelector('.analyzers-grid');
        grid.parentNode.insertBefore(filterContainer, grid);

        // Add filter styles
        this.addFilterStyles();

        // Setup filter functionality
        filterContainer.addEventListener('click', (e) => {
            const filterBtn = e.target.closest('.filter-btn');
            if (filterBtn) {
                this.setActiveFilter(filterBtn);
            }
        });
    }

    addFilterStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .filter-container {
                margin: 1rem 0 2rem 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 1rem;
            }
            
            .filter-buttons {
                display: flex;
                gap: 0.5rem;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .filter-btn {
                padding: 0.5rem 1rem;
                border: 2px solid var(--monokai-border);
                border-radius: 20px;
                background: var(--monokai-bg);
                color: var(--monokai-fg);
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                font-weight: 500;
                font-size: 0.9rem;
            }
            
            .filter-btn:hover {
                border-color: var(--monokai-accent);
                background: var(--monokai-bg-light);
                transform: translateY(-2px);
            }
            
            .filter-btn.active {
                background: var(--monokai-accent);
                color: var(--monokai-bg);
                border-color: var(--monokai-accent);
                transform: translateY(-2px);
            }
            
            .filter-stats {
                color: var(--monokai-comment);
                font-size: 0.9rem;
                text-align: center;
            }
        `;
        document.head.appendChild(style);
    }

    setupTooltips() {
        // Use a single tooltip element for better performance
        this.tooltip = this.createElement('div', 'tooltip');
        this.tooltip.style.cssText = `
            position: absolute;
            background: var(--monokai-bg);
            color: var(--monokai-fg);
            padding: 0.5rem 0.75rem;
            border-radius: 5px;
            font-size: 0.8rem;
            pointer-events: none;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
            border: 1px solid var(--monokai-border);
            box-shadow: 0 2px 8px var(--monokai-shadow);
        `;
        document.body.appendChild(this.tooltip);

        // Add tooltip functionality
        document.addEventListener('mouseover', this.handleTooltipShow.bind(this));
        document.addEventListener('mouseout', this.handleTooltipHide.bind(this));
    }

    setupKeyboardNavigation() {
        // Enhanced keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 'f':
                        e.preventDefault();
                        document.getElementById('analyzer-search')?.focus();
                        break;
                    case 'h':
                        e.preventDefault();
                        this.navigateToHome();
                        break;
                    case '1':
                    case '2':
                    case '3':
                    case '4':
                    case '5':
                    case '6':
                        e.preventDefault();
                        this.selectFilterByIndex(parseInt(e.key) - 1);
                        break;
                }
            } else if (e.key === 'Escape') {
                this.clearSearch();
            }
        });
    }

    setupPerformanceOptimizations() {
        // Preload critical resources
        this.preloadResources();
        
        // Setup virtual scrolling for large lists (future enhancement)
        this.setupVirtualScrolling();
        
        // Setup service worker for caching (future enhancement)
        this.setupServiceWorker();
    }

    preloadResources() {
        // Preload critical analyzer pages
        const criticalPages = ['csv-analyzer.html'];
        criticalPages.forEach(page => {
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = page;
            document.head.appendChild(link);
        });
    }

    setupVirtualScrolling() {
        // Placeholder for virtual scrolling implementation
        // This would be useful if we had many analyzers
        console.log('Virtual scrolling ready for future implementation');
    }

    setupServiceWorker() {
        // Placeholder for service worker implementation
        // This would cache resources for offline use
        console.log('Service worker ready for future implementation');
    }

    // Event Handlers
    handleClick(e) {
        const analyzerCard = e.target.closest('.analyzer-card');
        const backButton = e.target.closest('.back-button');
        const clearButton = e.target.closest('.clear-search');
        const suggestionItem = e.target.closest('.suggestion-item');

        if (analyzerCard) {
            this.handleAnalyzerClick(analyzerCard);
        } else if (backButton) {
            e.preventDefault();
            this.navigateToHome();
        } else if (clearButton) {
            this.clearSearch();
        } else if (suggestionItem) {
            this.selectSuggestion(suggestionItem.textContent);
        }
    }

    handleKeyboard(e) {
        // Handle keyboard navigation
        if (e.key === 'Enter' && e.target.id === 'analyzer-search') {
            this.performSearch();
        }
    }

    handleResize() {
        // Handle window resize
        this.updateLayout();
    }

    handleScroll() {
        // Handle scroll events for performance monitoring
        // Could be used for analytics or lazy loading
    }

    // Core Functionality
    filterAnalyzers() {
        const startTime = performance.now();
        
        this.filteredAnalyzers = this.analyzers.filter(analyzer => {
            const matchesSearch = this.searchTerm === '' || 
                analyzer.title.toLowerCase().includes(this.searchTerm) ||
                analyzer.description.toLowerCase().includes(this.searchTerm) ||
                analyzer.features.some(feature => feature.toLowerCase().includes(this.searchTerm)) ||
                analyzer.tags.some(tag => tag.toLowerCase().includes(this.searchTerm));
            
            const matchesFilter = this.currentFilter === 'all' ||
                analyzer.category === this.currentFilter ||
                (this.currentFilter === 'available' && analyzer.status === 'available');
            
            return matchesSearch && matchesFilter;
        });

        this.renderAnalyzers();
        
        const filterTime = performance.now() - startTime;
        console.log(`Filtering completed in ${filterTime.toFixed(2)}ms`);
    }

    renderAnalyzers() {
        const grid = document.querySelector('.analyzers-grid');
        if (!grid) return;

        // Use DocumentFragment for better performance
        const fragment = document.createDocumentFragment();
        
        if (this.filteredAnalyzers.length === 0) {
            fragment.appendChild(this.createNoResultsElement());
        } else {
            this.filteredAnalyzers.forEach(analyzer => {
                const card = this.createAnalyzerCard(analyzer);
                fragment.appendChild(card);
            });
        }

        // Clear and update grid
        grid.innerHTML = '';
        grid.appendChild(fragment);

        // Update filter stats
        this.updateFilterStats();

        // Observe new cards for animations
        this.observeCards();
    }

    createAnalyzerCard(analyzer) {
        const card = this.createElement('div', `analyzer-card ${analyzer.status === 'coming-soon' ? 'coming-soon' : ''}`);
        
        const featuresList = analyzer.features.map(feature => `<li>${feature}</li>`).join('');
        
        card.innerHTML = `
            <div class="analyzer-icon">
                <i class="${analyzer.icon}"></i>
            </div>
            <h3 class="analyzer-title">${analyzer.title}</h3>
            <p class="analyzer-description">${analyzer.description}</p>
            <ul class="analyzer-features">${featuresList}</ul>
            <div class="analyzer-meta">
                <span class="popularity">${analyzer.popularity}% popular</span>
                <span class="last-updated">Updated ${analyzer.lastUpdated}</span>
            </div>
            <a href="${analyzer.link}" class="analyzer-link" data-analyzer-id="${analyzer.id}">
                <i class="fas fa-${analyzer.status === 'available' ? 'chart-line' : 'clock'}"></i>
                ${analyzer.status === 'available' ? 'Launch Analyzer' : 'Coming Soon'}
            </a>
        `;

        // Add meta styles if not already added
        this.addMetaStyles();

        return card;
    }

    createNoResultsElement() {
        const noResults = this.createElement('div', 'no-results');
        noResults.innerHTML = `
            <i class="fas fa-search" style="font-size: 3rem; color: var(--monokai-comment); margin-bottom: 1rem;"></i>
            <h3 style="color: var(--monokai-fg); margin-bottom: 0.5rem;">No analyzers found</h3>
            <p style="color: var(--monokai-comment);">Try adjusting your search or filter criteria</p>
        `;
        return noResults;
    }

    addMetaStyles() {
        if (document.querySelector('style[data-meta-styles]')) return;
        
        const style = document.createElement('style');
        style.setAttribute('data-meta-styles', 'true');
        style.textContent = `
            .analyzer-meta {
                display: flex;
                justify-content: space-between;
                margin-bottom: 1rem;
                font-size: 0.8rem;
                color: var(--monokai-comment);
            }
            
            .popularity {
                color: var(--monokai-accent);
                font-weight: bold;
            }
        `;
        document.head.appendChild(style);
    }

    // Search and Filter Methods
    showSuggestions(query) {
        const suggestions = document.getElementById('search-suggestions');
        if (!suggestions) return;

        const matchingAnalyzers = this.analyzers.filter(analyzer => 
            analyzer.title.toLowerCase().includes(query.toLowerCase()) ||
            analyzer.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
        ).slice(0, 5);

        if (matchingAnalyzers.length > 0) {
            suggestions.innerHTML = matchingAnalyzers.map(analyzer => 
                `<div class="suggestion-item" data-analyzer="${analyzer.title}">${analyzer.title}</div>`
            ).join('');
            suggestions.style.display = 'block';
        } else {
            this.hideSuggestions();
        }
    }

    hideSuggestions() {
        const suggestions = document.getElementById('search-suggestions');
        if (suggestions) {
            suggestions.style.display = 'none';
        }
    }

    selectSuggestion(text) {
        const searchInput = document.getElementById('analyzer-search');
        if (searchInput) {
            searchInput.value = text;
            this.searchTerm = text.toLowerCase();
            this.filterAnalyzers();
            this.hideSuggestions();
        }
    }

    setActiveFilter(filterBtn) {
        document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
        filterBtn.classList.add('active');
        this.currentFilter = filterBtn.dataset.filter;
        this.filterAnalyzers();
    }

    selectFilterByIndex(index) {
        const filterBtns = document.querySelectorAll('.filter-btn');
        if (filterBtns[index]) {
            this.setActiveFilter(filterBtns[index]);
        }
    }

    updateSearchUI() {
        const clearButton = document.getElementById('clear-search');
        if (clearButton) {
            clearButton.style.display = this.searchTerm ? 'block' : 'none';
        }
    }

    updateFilterStats() {
        const stats = document.getElementById('filter-stats');
        if (stats) {
            const total = this.analyzers.length;
            const filtered = this.filteredAnalyzers.length;
            stats.textContent = `Showing ${filtered} of ${total} analyzers`;
        }
    }

    // Analyzer Interaction Methods
    handleAnalyzerClick(card) {
        const link = card.querySelector('.analyzer-link');
        if (link && link.href !== '#') {
            this.animateCardClick(card, () => {
                window.location.href = link.href;
            });
        } else {
            this.showComingSoonMessage(card);
        }
    }

    animateCardClick(card, callback) {
        card.style.transform = 'scale(0.95)';
        this.raf(() => {
            card.style.transform = '';
            if (callback) callback();
        }, 150);
    }

    showComingSoonMessage(card) {
        const title = card.querySelector('.analyzer-title').textContent;
        
        // Create modal with better performance
        const modal = this.createModal(title);
        document.body.appendChild(modal);

        // Setup modal event listeners
        this.setupModalEvents(modal);
    }

    createModal(title) {
        const modal = this.createElement('div', 'coming-soon-modal');
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="close-modal" aria-label="Close modal">&times;</button>
                </div>
                <div class="modal-body">
                    <i class="fas fa-clock" style="font-size: 3rem; color: var(--monokai-accent); margin-bottom: 1rem;"></i>
                    <p>This analyzer is currently under development and will be available soon!</p>
                    <p>Stay tuned for updates.</p>
                </div>
                <div class="modal-footer">
                    <button class="modal-btn">Got it!</button>
                </div>
            </div>
        `;

        // Add modal styles
        this.addModalStyles();

        return modal;
    }

    addModalStyles() {
        if (document.querySelector('style[data-modal-styles]')) return;
        
        const style = document.createElement('style');
        style.setAttribute('data-modal-styles', 'true');
        style.textContent = `
            .coming-soon-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
                animation: fadeIn 0.3s ease;
                backdrop-filter: blur(5px);
            }
            
            .modal-content {
                background: var(--monokai-bg);
                border: 1px solid var(--monokai-border);
                border-radius: 15px;
                padding: 2rem;
                max-width: 400px;
                width: 90%;
                text-align: center;
                animation: slideIn 0.3s ease;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            }
            
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }
            
            .close-modal {
                background: none;
                border: none;
                color: var(--monokai-comment);
                font-size: 1.5rem;
                cursor: pointer;
                padding: 0.5rem;
                border-radius: 50%;
                transition: all 0.3s ease;
            }
            
            .close-modal:hover {
                background: var(--monokai-bg-light);
                color: var(--monokai-accent);
            }
            
            .modal-btn {
                background: var(--monokai-accent);
                color: var(--monokai-bg);
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 25px;
                cursor: pointer;
                font-weight: bold;
                margin-top: 1rem;
                transition: all 0.3s ease;
            }
            
            .modal-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px var(--monokai-glow);
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes slideIn {
                from { transform: translateY(-50px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    setupModalEvents(modal) {
        const closeModal = () => {
            modal.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => modal.remove(), 300);
        };

        modal.querySelector('.close-modal').addEventListener('click', closeModal);
        modal.querySelector('.modal-btn').addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });

        // Add fadeOut animation
        if (!document.querySelector('style[data-fadeout]')) {
            const style = document.createElement('style');
            style.setAttribute('data-fadeout', 'true');
            style.textContent = `
                @keyframes fadeOut {
                    from { opacity: 1; }
                    to { opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // Tooltip Methods
    handleTooltipShow(e) {
        const card = e.target.closest('.analyzer-card');
        if (card) {
            const title = card.querySelector('.analyzer-title').textContent;
            const status = card.classList.contains('coming-soon') ? 'Coming Soon' : 'Available';
            const popularity = this.analyzers.find(a => a.title === title)?.popularity || 0;
            
            this.tooltip.textContent = `${title} - ${status} (${popularity}% popular)`;
            this.tooltip.style.opacity = '1';
            
            const rect = card.getBoundingClientRect();
            this.tooltip.style.left = rect.left + 'px';
            this.tooltip.style.top = (rect.top - 40) + 'px';
        }
    }

    handleTooltipHide(e) {
        if (!e.target.closest('.analyzer-card')) {
            this.tooltip.style.opacity = '0';
        }
    }

    // Navigation Methods
    navigateToHome() {
        this.animateExit(() => {
            window.location.href = '../index.html';
        });
    }

    animateExit(callback) {
        document.body.style.transition = 'opacity 0.3s ease';
        document.body.style.opacity = '0';
        setTimeout(callback, 300);
    }

    clearSearch() {
        const searchInput = document.getElementById('analyzer-search');
        if (searchInput) {
            searchInput.value = '';
            this.searchTerm = '';
            this.filterAnalyzers();
            this.hideSuggestions();
            searchInput.focus();
        }
    }

    // Utility Methods
    createElement(tag, className = '') {
        const element = document.createElement(tag);
        if (className) {
            element.className = className;
        }
        return element;
    }

    raf(callback, delay = 0) {
        if (delay > 0) {
            setTimeout(() => requestAnimationFrame(callback), delay);
        } else {
            requestAnimationFrame(callback);
        }
    }

    throttle(func, limit) {
        if (this.throttledFunctions.has(func)) {
            return this.throttledFunctions.get(func);
        }
        
        let inThrottle;
        const throttled = function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
        
        this.throttledFunctions.set(func, throttled);
        return throttled;
    }

    debounce(func, wait) {
        return (...args) => {
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(() => func.apply(this, args), wait);
        };
    }

    observeCards() {
        if (this.observer) {
            document.querySelectorAll('.analyzer-card:not(.animate-in)').forEach(card => {
                this.observer.observe(card);
            });
        }
    }

    updateLayout() {
        // Handle responsive layout updates
        const grid = document.querySelector('.analyzers-grid');
        if (grid) {
            // Force reflow for better performance
            grid.style.display = 'none';
            grid.offsetHeight; // Trigger reflow
            grid.style.display = '';
        }
    }

    performSearch() {
        const searchInput = document.getElementById('analyzer-search');
        if (searchInput) {
            this.searchTerm = searchInput.value.toLowerCase();
            this.filterAnalyzers();
            this.hideSuggestions();
        }
    }

    // Cleanup method
    destroy() {
        if (this.observer) {
            this.observer.disconnect();
        }
        
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }
        
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        // Remove event listeners
        document.removeEventListener('click', this.handleClick);
        document.removeEventListener('keydown', this.handleKeyboard);
        window.removeEventListener('resize', this.handleResize);
        window.removeEventListener('scroll', this.handleScroll);
    }
}

// Initialize the page when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Add loading state
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    // Initialize the page
    window.analyzersPage = new AnalyzersPage();
    
    // Show page when loaded
    window.addEventListener('load', () => {
        document.body.style.opacity = '1';
    });
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.analyzersPage) {
        window.analyzersPage.destroy();
    }
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AnalyzersPage;
}
