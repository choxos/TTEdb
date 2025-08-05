// Empty service worker file to prevent 404 errors
// This file is required by some themes but not actively used

self.addEventListener('install', function(event) {
  // Skip waiting to activate immediately
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  // Clean up old caches if any
  event.waitUntil(self.clients.claim());
});

// No actual service worker functionality needed