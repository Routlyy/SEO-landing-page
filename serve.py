#!/usr/bin/env python3
"""Local dev server matching production (Vercel): gzip + cache headers.
Run: python3 serve.py [port]  (default 8080)"""
import gzip, http.server, io, sys, functools

COMPRESS = ('.html', '.css', '.js', '.svg', '.xml', '.txt', '.json', '.ico')

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        if self.path.startswith('/assets/'):
            self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
        else:
            self.send_header('Cache-Control', 'public, max-age=0, must-revalidate')
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        if path.endswith('/'): path += 'index.html'
        import os
        if '.' not in os.path.basename(path):
            for ext in ('.html',):
                if os.path.exists(path + ext): path += ext; break
        if not os.path.exists(path) or os.path.isdir(path):
            return super().send_head()
        ext = os.path.splitext(path.split('?')[0])[1].lower()
        accept = self.headers.get('Accept-Encoding', '')
        if ext in COMPRESS and 'gzip' in accept:
            with open(path, 'rb') as f: raw = f.read()
            data = gzip.compress(raw, 6)
            self.send_response(200)
            self.send_header('Content-Type', self.guess_type(path))
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            return io.BytesIO(data)
        return super().send_head()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    http.server.ThreadingHTTPServer(('', port), Handler).serve_forever()
