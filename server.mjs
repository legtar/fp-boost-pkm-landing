import { createReadStream, statSync } from "node:fs";
import { createServer } from "node:http";
import { extname, join, normalize, sep } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL(".", import.meta.url));
const port = Number(process.env.PORT || 8123);
const host = process.env.HOST || "127.0.0.1";

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".pdf": "application/pdf",
};

function sendText(response, status, text) {
  response.writeHead(status, {
    "Content-Type": "text/plain; charset=utf-8",
    "Content-Length": Buffer.byteLength(text),
  });
  response.end(text);
}

function resolvePath(requestUrl) {
  const url = new URL(requestUrl, `http://${host}:${port}`);
  const decodedPath = decodeURIComponent(url.pathname);
  const relativePath = decodedPath === "/" ? "index.html" : decodedPath.replace(/^\/+/, "");
  const filePath = normalize(join(root, relativePath));
  const rootWithSep = root.endsWith(sep) ? root : `${root}${sep}`;

  if (!filePath.startsWith(rootWithSep)) {
    return null;
  }

  return filePath;
}

const server = createServer((request, response) => {
  if (!["GET", "HEAD"].includes(request.method || "")) {
    sendText(response, 405, "Method not allowed");
    return;
  }

  const filePath = resolvePath(request.url || "/");
  if (!filePath) {
    sendText(response, 403, "Forbidden");
    return;
  }

  let fileStat;
  try {
    fileStat = statSync(filePath);
  } catch {
    sendText(response, 404, "File not found");
    return;
  }

  if (!fileStat.isFile()) {
    sendText(response, 404, "File not found");
    return;
  }

  response.writeHead(200, {
    "Content-Type": mimeTypes[extname(filePath).toLowerCase()] || "application/octet-stream",
    "Content-Length": fileStat.size,
    "Cache-Control": "no-cache",
  });

  if (request.method === "HEAD") {
    response.end();
    return;
  }

  createReadStream(filePath).pipe(response);
});

server.listen(port, host, () => {
  console.log(`Serving ${root} at http://${host}:${port}/`);
});
