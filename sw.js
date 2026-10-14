/* 바로가기(앱 설치)용 서비스 워커.
   항상 인터넷에서 새 파일을 먼저 받고(그래서 단어·코드 갱신이 바로 반영됨),
   인터넷이 끊겼을 때만 마지막으로 받아 둔 사본을 보여 줍니다. 이 사이트 파일만 다룹니다. */
const CACHE = "sueo-v1";
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  e.respondWith(
    fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return res;
    }).catch(() => caches.match(req, {ignoreSearch: true}))
  );
});
