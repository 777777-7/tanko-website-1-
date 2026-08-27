# -*- coding: utf-8 -*-
"""
Local preview server for the Primaxs / Tanko Malaysia site.

The site is now built root-hosted (BASE_URL=/), which matches a Cloudflare Pages
custom domain. This server simply serves ./docs at http://localhost:PORT/ so the
local preview behaves exactly like the deployed site (links, CSS, JS, images).

Usage:
    python serve_local.py            # port 8000
    python serve_local.py 8080       # custom port
"""
import http.server
import os
import socketserver
import sys
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "docs")


class PreviewHandler(http.server.SimpleHTTPRequestHandler):
    """Serve ./docs as the site root."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST, **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    host = "127.0.0.1"
    try:
        with socketserver.ThreadingTCPServer((host, port), PreviewHandler) as httpd:
            url = "http://localhost:%d/" % port
            print("=" * 56)
            print("  Primaxs / Tanko Malaysia - local preview")
            print("  Serving: %s" % url)
            print("  Docs folder: %s" % DIST)
            print("  Press Ctrl+C to stop the server.")
            print("=" * 56)
            webbrowser.open(url)
            httpd.serve_forever()
    except OSError as e:
        print("Could not start server on port %d: %s" % (port, e))
        print("Try a different port, e.g.  python serve_local.py 8080")
        sys.exit(1)
