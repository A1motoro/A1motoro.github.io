// Service Worker for Analyzers Page - Caching and Performance
const CACHE_NAME = 'analyzers-v1.0.0';
const STATIC_CACHE = 'analyzers-static-v1.0.0';
const DYNAMIC_CACHE = 'analyzers-dynamic-v1.0.0';

// Files to cache immediately
const STATIC_FILES = [
    '/',
    '/analyzers/',
    '/analyzers/index.html',
    '/analyzers/js/analyzers-page.js',
    '/analyzers/js/performance-monitor.js',
    '/core-framework/themes/monokai-core.css',
    '/core-framework/components/navigation.html',
    '/core-framework/components/footer.html',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
];

// Files to cache on demand
const DYNAMIC_FILES = [
    '/analyzers/csv-analyzer.html',
    '/analyzers/csv-analyzer-js.html'
];

// Install event - cache static files
self.addEventListener('install', (event) => {
    console.log('Service Worker installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Caching static files...');
                return cache.addAll(STATIC_FILES);
            })
            .then(() => {
                console.log('Static files cached successfully');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('Error caching static files:', error);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('Service Worker activating...');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                            console.log('Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('Service Worker activated');
                return self.clients.claim();
            })
    );
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Skip chrome-extension and other non-http requests
    if (!url.protocol.startsWith('http')) {
        return;
    }
    
    event.respondWith(
        caches.match(request)
            .then(cachedResponse => {
                // Return cached version if available
                if (cachedResponse) {
                    console.log('Serving from cache:', request.url);
                    return cachedResponse;
                }
                
                // Otherwise fetch from network
                return fetch(request)
                    .then(response => {
                        // Don't cache non-successful responses
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        
                        // Clone the response
                        const responseToCache = response.clone();
                        
                        // Cache dynamic files
                        if (shouldCache(request.url)) {
                            caches.open(DYNAMIC_CACHE)
                                .then(cache => {
                                    cache.put(request, responseToCache);
                                    console.log('Cached dynamic file:', request.url);
                                });
                        }
                        
                        return response;
                    })
                    .catch(error => {
                        console.error('Fetch failed:', error);
                        
                        // Return offline page for navigation requests
                        if (request.mode === 'navigate') {
                            return caches.match('/analyzers/index.html');
                        }
                        
                        // Return cached version if available
                        return caches.match(request);
                    });
            })
    );
});

// Background sync for offline actions
self.addEventListener('sync', (event) => {
    if (event.tag === 'background-sync') {
        console.log('Background sync triggered');
        event.waitUntil(doBackgroundSync());
    }
});

// Push notifications (for future use)
self.addEventListener('push', (event) => {
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body,
            icon: '/analyzers/icon-192x192.png',
            badge: '/analyzers/badge-72x72.png',
            vibrate: [100, 50, 100],
            data: {
                dateOfArrival: Date.now(),
                primaryKey: data.primaryKey
            },
            actions: [
                {
                    action: 'explore',
                    title: 'Explore',
                    icon: '/analyzers/action-explore.png'
                },
                {
                    action: 'close',
                    title: 'Close',
                    icon: '/analyzers/action-close.png'
                }
            ]
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/analyzers/')
        );
    }
});

// Helper functions
function shouldCache(url) {
    // Cache HTML, CSS, JS, and image files
    const cacheableExtensions = ['.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.woff', '.woff2'];
    return cacheableExtensions.some(ext => url.includes(ext));
}

function doBackgroundSync() {
    // Perform background sync tasks
    return new Promise((resolve) => {
        console.log('Performing background sync...');
        // Add your background sync logic here
        resolve();
    });
}

// Cache management utilities
function clearAllCaches() {
    return caches.keys().then(cacheNames => {
        return Promise.all(
            cacheNames.map(cacheName => caches.delete(cacheName))
        );
    });
}

function getCacheSize() {
    return caches.keys().then(cacheNames => {
        return Promise.all(
            cacheNames.map(cacheName => 
                caches.open(cacheName).then(cache => 
                    cache.keys().then(keys => ({ name: cacheName, size: keys.length }))
                )
            )
        );
    });
}

// Message handling for cache management
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        clearAllCaches().then(() => {
            event.ports[0].postMessage({ success: true });
        });
    }
    
    if (event.data && event.data.type === 'GET_CACHE_SIZE') {
        getCacheSize().then(sizes => {
            event.ports[0].postMessage({ sizes });
        });
    }
});

console.log('Service Worker loaded successfully');
