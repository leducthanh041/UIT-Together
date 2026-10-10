"""Build, watch source files and serve the generated static website locally."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import threading
import time
import subprocess
import sys
from build import ROOT, build

def fingerprint():
    result = []
    for p in sorted((ROOT / "src").rglob("*")):
        if p.suffix == ".tmp":
            continue
        try:
            if p.is_file():
                stat = p.stat()
                result.append((str(p), stat.st_mtime_ns, stat.st_size))
        except FileNotFoundError:
            continue  # Atomic data replacement can finish while scanning.
    return result

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

def sync_conferences(stop):
    """Refresh on startup and every six hours without blocking local previews."""
    while not stop.is_set():
        process = subprocess.Popen([sys.executable, str(ROOT / "scripts/update_conferences.py")], cwd=ROOT)
        while process.poll() is None:
            if stop.wait(0.5):
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                return
        print("Conference sources checked; unavailable sources retain their last verified dates.", flush=True)
        if stop.wait(6 * 3600):
            return

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
    parser.add_argument("--no-conference-sync", action="store_true", help="Disable periodic official-source checks for offline editing")
    args = parser.parse_args()
    directory = build()
    with ThreadingHTTPServer((args.host, args.port), partial(Handler, directory=str(directory))) as server:
        stop = threading.Event()
        thread = threading.Thread(target=watch, args=(stop,), daemon=True)
        thread.start()
        sync_thread = None
        if not args.no_conference_sync:
            sync_thread = threading.Thread(target=sync_conferences, args=(stop,), daemon=True)
            sync_thread.start()
        print(f"Local preview: http://{args.host}:{args.port} — Ctrl+C to stop", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            stop.set()
            thread.join()
            if sync_thread:
                sync_thread.join(timeout=5)
