// {"Content-Type": "text/javascript", "Service-Worker-Allowed": "/"}
self.addEventListener("fetch", (event) => {
    event.respondWith(handle_fetch_event(event))
})

async function handle_fetch_event(event) {
    return await fetch("/hijack/")
}
