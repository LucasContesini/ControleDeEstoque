// Service Worker para PWA
const CACHE_NAME = 'controle-estoque-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/app.js'
];

// Instalar Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        // Tentar adicionar URLs ao cache, ignorar erros
        return Promise.allSettled(
          urlsToCache.map(url => cache.add(url).catch(() => {}))
        );
      })
      .then(() => {
        // Forçar ativação imediata
        return self.skipWaiting();
      })
  );
});

// Ativar Service Worker
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Interceptar requisições
self.addEventListener('fetch', (event) => {
  // Não cachear requisições de API
  if (event.request.url.includes('/api/')) {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Retornar do cache se disponível, senão buscar na rede
        return response || fetch(event.request);
      })
  );
});

