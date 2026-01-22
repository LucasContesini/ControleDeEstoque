// Service Worker para forçar atualização e quebrar cache do navegador mobile
// Versão: 2026-01-22-v1

const CACHE_NAME = 'controle-estoque-v1';
const FORCE_UPDATE_INTERVAL = 300000; // 5 minutos

// Instalar Service Worker
self.addEventListener('install', (event) => {
    // Forçar ativação imediata
    self.skipWaiting();
});

// Ativar Service Worker
self.addEventListener('activate', (event) => {
    // Limpar caches antigos
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
    // Forçar controle imediato
    return self.clients.claim();
});

// Interceptar requisições
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);
    
    // Para HTML, sempre buscar do servidor (nunca cachear)
    if (event.request.destination === 'document' || 
        url.pathname === '/' || 
        event.request.headers.get('accept')?.includes('text/html')) {
        event.respondWith(
            fetch(event.request, {
                cache: 'no-store',
                headers: {
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
            }).catch(() => {
                // Se falhar, tentar buscar do cache como fallback
                return caches.match(event.request);
            })
        );
        return;
    }
    
    // Para outros recursos, usar estratégia network-first
    event.respondWith(
        fetch(event.request, {
            cache: 'no-store'
        }).catch(() => {
            return caches.match(event.request);
        })
    );
});

// Verificar atualizações periodicamente
setInterval(() => {
    self.registration.update();
}, FORCE_UPDATE_INTERVAL);
