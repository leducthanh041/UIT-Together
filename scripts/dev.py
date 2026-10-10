"""Build, watch source files and serve the generated static website locally."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import threading
import time
from build import ROOT, build

def fingerprint():
    return [(str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in sorted((ROOT / "src").rglob("*")) if p.is_file()]

def watch(stop):
    previous = fingerprint()
    while not stop.wait(1):
        current = fingerprint()
        if current != previous:
            try:
                build()
                print("Updated. Refresh your browser.", flush=True)
            except Exception as error:
                print(f"Build failed; previous output retained: {error}", flush=True)
            previous = current

class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()
    def list_directory(self, path):
        self.send_error(404)
        return None
    def translate_path(self, path):
        result = super().translate_path(path)
        from pathlib import Path
        candidate = Path(result)
        if not candidate.exists() and candidate.with_suffix(".html").is_file():
            return str(candidate.with_suffix(".html"))
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    directory = build()
    with ThreadingHTTPServer((args.host, args.port), partial(Handler, directory=str(directory))) as server:
        stop = threading.Event()
        thread = threading.Thread(target=watch, args=(stop,), daemon=True)
        thread.start()
        print(f"Local preview: http://{args.host}:{args.port} — Ctrl+C to stop", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            stop.set()
            thread.join()
