// Service Worker（オフライン対応）v0.9
// - ページ本体（同一オリジン）：ネット優先・失敗時はキャッシュ（更新が確実に届く）
// - CDN（transformers.js / ONNX Runtime / Tesseract.js本体）：キャッシュ優先（2回目以降はオフラインで動く）
// - Hugging Faceのモデル・Tesseractの日本語データ：各ライブラリ自身がキャッシュするため素通し

const VER = "v0.9";
const SHELL = "ops-shell-" + VER;
const CDN = "ops-cdn-" + VER;
const SHELL_URLS = ["./", "./index.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(SHELL).then((c) => c.addAll(SHELL_URLS)).catch(() => {}).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== SHELL && k !== CDN).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  let url;
  try { url = new URL(req.url); } catch (err) { return; }

  // 同一オリジン（ページ本体・アイコン等）：ネット優先、失敗時キャッシュ
  if (url.origin === self.location.origin) {
    e.respondWith(
      fetch(req)
        .then((res) => {
          if (res && res.ok) {
            const copy = res.clone();
            caches.open(SHELL).then((c) => c.put(req, copy)).catch(() => {});
          }
          return res;
        })
        .catch(() =>
          caches.match(req).then((r) => r || (req.mode === "navigate" ? caches.match("./index.html") : Response.error()))
        )
    );
    return;
  }

  // CDN（jsdelivr）：キャッシュ優先・初回取得時に保存
  if (url.hostname === "cdn.jsdelivr.net") {
    e.respondWith(
      caches.match(req).then(
        (hit) =>
          hit ||
          fetch(req).then((res) => {
            if (res && res.ok) {
              const copy = res.clone();
              caches.open(CDN).then((c) => c.put(req, copy)).catch(() => {});
            }
            return res;
          })
      )
    );
    return;
  }
  // それ以外（huggingface.co / tessdata 等）は素通し：
  // transformers.js はモデルを、Tesseract.js は言語データを、それぞれ自前のキャッシュに保存するため二重保存を避ける
});
