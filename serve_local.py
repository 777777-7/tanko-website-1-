# -*- coding: utf-8 -*-
"""
Local preview server for the Primaxs / Tanko Malaysia site.

The site is built with BASE_URL=/tanko-website-1-/ so it can be hosted under a
GitHub Pages sub-path. This server maps:
    http://localhost:PORT/tanko-website-1-/*  ->  ./docs/*
so the local preview behaves exactly like the deployed site (links, CSS, JS
and images all resolve). It also auto-opens your default browser.

Usage:
    python serve_local.py            # port 8000
    python serve_local.py 8080       # custom port
"""
import http.server
import os
import socketserver
import sys
import urllib.parse
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "docs")
PREFIX = "/tanko-website-1-"


class PreviewHandler(http.server.SimpleHTTPRequestHandler):
    """Serve ./docs under the /tanko-website-1- path prefix."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST, **kwargs)

    def translate_path(self, path):
        # Strip the site prefix, then resolve inside docs/ (SimpleHTTPRequestHandler
        # joins with self.directory = DIST).
        parsed = urllib.parse.urlparse(path)
        p = parsed.path
        if p.startswith(PREFIX):
            p = p[len(PREFIX):]
        if not p.startswith("/"):
            p = "/" + p
        return super().translate_path(p)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        p = parsed.path
        if p == "/":
            # Root -> redirect to the site sub-path so the homepage loads.
            self.send_response(301)
            self.send_header("Location", PREFIX + "/")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if not p.startswith(PREFIX):
            self.send_error(404, "Not found — this site lives under " + PREFIX + "/")
            return
        # Directory without trailing slash -> keep the prefix intact.
        rel = p[len(PREFIX):].lstrip("/")
        full = os.path.join(DIST, rel.replace("/", os.sep))
        if os.path.isdir(full) and not p.endswith("/"):
            self.send_response(301)
            self.send_header("Location", p + "/")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        return super().do_GET()

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    host = "127.0.0.1"
    handler = PreviewHandler
    try:
        with socketserver.ThreadingTCPServer((host, port), handler) as httpd:
            url = "http://localhost:%d%s/" % (port, PREFIX)
            print("=" * 60)
            print("  Primaxs / Tanko Malaysia — local preview")
            print("  Serving: %s" % url)
            print("  Docs folder: %s" % DIST)
            print("  Press Ctrl+C to stop the server.")
            print("=" * 60)
            webbrowser.open(url)
            httpd.serve_forever()
    except OSError as e:
        print("Could not start server on port %d: %s" % (port, e))
        print("Try a different port, e.g.  python serve_local.py 8080")
        sys.exit(1)
