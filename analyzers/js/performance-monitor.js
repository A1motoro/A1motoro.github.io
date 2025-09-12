// Performance Monitoring for Analyzers Page
class PerformanceMonitor {
    constructor() {
        this.metrics = {
            pageLoad: 0,
            componentLoad: 0,
            searchTime: 0,
            filterTime: 0,
            renderTime: 0,
            animationTime: 0
        };
        
        this.startTimes = new Map();
        this.observers = new Map();
        
        this.init();
    }

    init() {
        this.setupPerformanceObserver();
        this.setupResourceTiming();
        this.setupUserTiming();
        this.setupMemoryMonitoring();
        this.setupErrorTracking();
    }

    setupPerformanceObserver() {
        if ('PerformanceObserver' in window) {
            // Observe navigation timing
            const navObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    if (entry.entryType === 'navigation') {
                        this.metrics.pageLoad = entry.loadEventEnd - entry.loadEventStart;
                        console.log(`Page load time: ${this.metrics.pageLoad.toFixed(2)}ms`);
                    }
                });
            });
            navObserver.observe({ entryTypes: ['navigation'] });

            // Observe paint timing
            const paintObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    if (entry.name === 'first-contentful-paint') {
                        console.log(`First Contentful Paint: ${entry.startTime.toFixed(2)}ms`);
                    }
                    if (entry.name === 'largest-contentful-paint') {
                        console.log(`Largest Contentful Paint: ${entry.startTime.toFixed(2)}ms`);
                    }
                });
            });
            paintObserver.observe({ entryTypes: ['paint'] });

            this.observers.set('navigation', navObserver);
            this.observers.set('paint', paintObserver);
        }
    }

    setupResourceTiming() {
        // Monitor resource loading performance
        window.addEventListener('load', () => {
            const resources = performance.getEntriesByType('resource');
            const totalResourceTime = resources.reduce((sum, resource) => {
                return sum + (resource.responseEnd - resource.startTime);
            }, 0);
            
            console.log(`Total resource load time: ${totalResourceTime.toFixed(2)}ms`);
            console.log(`Number of resources: ${resources.length}`);
            
            // Identify slow resources
            const slowResources = resources.filter(resource => 
                (resource.responseEnd - resource.startTime) > 1000
            );
            
            if (slowResources.length > 0) {
                console.warn('Slow resources detected:', slowResources.map(r => ({
                    name: r.name,
                    duration: (r.responseEnd - r.startTime).toFixed(2) + 'ms'
                })));
            }
        });
    }

    setupUserTiming() {
        // Custom performance marks and measures
        this.mark = (name) => {
            performance.mark(name);
            this.startTimes.set(name, performance.now());
        };

        this.measure = (name, startMark, endMark) => {
            if (performance.getEntriesByName(startMark).length > 0 && 
                performance.getEntriesByName(endMark).length > 0) {
                performance.measure(name, startMark, endMark);
                const measure = performance.getEntriesByName(name)[0];
                console.log(`${name}: ${measure.duration.toFixed(2)}ms`);
                return measure.duration;
            }
        };

        this.endMark = (name) => {
            const startTime = this.startTimes.get(name);
            if (startTime) {
                const duration = performance.now() - startTime;
                console.log(`${name}: ${duration.toFixed(2)}ms`);
                this.startTimes.delete(name);
                return duration;
            }
        };
    }

    setupMemoryMonitoring() {
        if ('memory' in performance) {
            setInterval(() => {
                const memory = performance.memory;
                console.log('Memory usage:', {
                    used: (memory.usedJSHeapSize / 1024 / 1024).toFixed(2) + 'MB',
                    total: (memory.totalJSHeapSize / 1024 / 1024).toFixed(2) + 'MB',
                    limit: (memory.jsHeapSizeLimit / 1024 / 1024).toFixed(2) + 'MB'
                });
            }, 30000); // Check every 30 seconds
        }
    }

    setupErrorTracking() {
        // Track JavaScript errors
        window.addEventListener('error', (event) => {
            console.error('JavaScript Error:', {
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                error: event.error
            });
        });

        // Track unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled Promise Rejection:', event.reason);
        });
    }

    // Performance tracking methods
    trackSearch(searchFunction) {
        return (...args) => {
            this.mark('search-start');
            const result = searchFunction.apply(this, args);
            this.metrics.searchTime = this.endMark('search-start');
            return result;
        };
    }

    trackFilter(filterFunction) {
        return (...args) => {
            this.mark('filter-start');
            const result = filterFunction.apply(this, args);
            this.metrics.filterTime = this.endMark('filter-start');
            return result;
        };
    }

    trackRender(renderFunction) {
        return (...args) => {
            this.mark('render-start');
            const result = renderFunction.apply(this, args);
            this.metrics.renderTime = this.endMark('render-start');
            return result;
        };
    }

    trackAnimation(animationFunction) {
        return (...args) => {
            this.mark('animation-start');
            const result = animationFunction.apply(this, args);
            this.metrics.animationTime = this.endMark('animation-start');
            return result;
        };
    }

    // Performance reporting
    generateReport() {
        const report = {
            timestamp: new Date().toISOString(),
            metrics: this.metrics,
            userAgent: navigator.userAgent,
            connection: navigator.connection ? {
                effectiveType: navigator.connection.effectiveType,
                downlink: navigator.connection.downlink,
                rtt: navigator.connection.rtt
            } : null,
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            }
        };

        console.log('Performance Report:', report);
        return report;
    }

    // Cleanup
    destroy() {
        this.observers.forEach(observer => observer.disconnect());
        this.observers.clear();
        this.startTimes.clear();
    }
}

// Initialize performance monitoring
window.performanceMonitor = new PerformanceMonitor();

// Export for external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceMonitor;
}
