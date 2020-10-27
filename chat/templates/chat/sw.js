// --------------------PWA--------------------
self.addEventListener("install", function (event) {
    event.waitUntil(preLoad());
});

var preLoad = async function () {
    console.log("Installing web app");
    const cache = await caches.open("offline");
    console.log("caching index and important routes");
    return cache.addAll(["/users/", "/users/all", "/", "/users/about/",]);
};

self.addEventListener("fetch", function (event) {
    event.respondWith(checkResponse(event.request).catch(function () {
        return returnFromCache(event.request);
    }));
    event.waitUntil(addToCache(event.request));
});

var checkResponse = function (request) {
    return new Promise(function (fulfill, reject) {
        fetch(request).then(function (response) {
            if (response.status !== 404) {
                fulfill(response);
            } else {
                reject();
            }
        }, reject);
    });
};

var addToCache = async function (request) {
    const cache = await caches.open("offline");
    const response = await fetch(request);
    console.log(response.url + " was cached");
    return cache.put(request, response);
};

var returnFromCache = async function (request) {
    const cache = await caches.open("offline");
    const matching = await cache.match(request);
    if (!matching || matching.status == 404) {
        return cache.match("offline.html");
    } else {
        return matching;
    }
};
// --------------------END PWA--------------------

// --------------------PUSH NOTIFICATIONS--------------------
/* self.addEventListener('push', function (event) {
    console.log('[Service Worker] Push Received.');
    console.log(`[Service Worker] Push had this data: "${event.data.text()}"`);

    const title = 'Orgachat';
    const options = {
        body: 'You received a message.',
        icon: 'static/chat/img/favicon.png',
        badge: 'static/chat/img/favicon.png',
        vibrate: [100, 50, 100],
    };
    const notificationPromise = self.registration.showNotification(title, options);
    event.waitUntil(notificationPromise);
});

self.addEventListener('notificationclick', function (event) {
    console.log('[Service Worker] Notification click Received.');

    event.notification.close();

    event.waitUntil(
        clients.openWindow('https://www.orgachat.com')
    );
}); */
// --------------------END PUSH NOTIFICATIONS--------------------

// -------------------BADGE----------------------

// -------------------END BADGE----------------------