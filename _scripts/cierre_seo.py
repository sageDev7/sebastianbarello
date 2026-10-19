"""Cierre SEO de Sebastian Barello SIN .htaccess (los links siguen siendo .html, sirve en cualquier hosting estático).
Correr cuando esté el dominio:  python _scripts/cierre_seo.py https://dominio.com.ar
- og:url, canonical, og:image y twitter:image absolutos (WhatsApp/Facebook no leen rutas relativas)
- sitemap.xml y robots.txt con la línea Sitemap
Idempotente: se puede volver a correr."""
import os, re, sys
from datetime import date
if len(sys.argv) < 2 or not sys.argv[1].startswith("http"):
    sys.exit("Uso: python _scripts/cierre_seo.py https://dominio.com.ar")
DOM = sys.argv[1].rstrip("/")
D = os.path.join(os.path.dirname(__file__), "..")
PAGES = {"index.html": ("/", "1.0"), "privacidad.html": ("/privacidad.html", "0.3")}

def set_tag(s, pat, tag):
    return re.sub(pat, tag, s, count=1) if re.search(pat, s) else s.replace("</head>", tag + "\n</head>", 1)

for f, (path, _) in PAGES.items():
    p = os.path.join(D, f); s = open(p, encoding="utf8").read()
    url = DOM + path
    s = set_tag(s, r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">')
    s = set_tag(s, r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">')
    s = set_tag(s, r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{DOM}/og.png">')
    s = set_tag(s, r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{DOM}/og.png">')
    open(p, "w", encoding="utf8").write(s); print("ok", f)
hoy = date.today().isoformat()
urls = "\n".join(f"  <url><loc>{DOM}{p}</loc><lastmod>{hoy}</lastmod><priority>{pr}</priority></url>" for p, pr in PAGES.values())
open(os.path.join(D, "sitemap.xml"), "w", encoding="utf8").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
open(os.path.join(D, "robots.txt"), "w", encoding="utf8").write(f"User-agent: *\nAllow: /\nDisallow: /_scripts/\n\nSitemap: {DOM}/sitemap.xml\n")
print("ok sitemap.xml y robots.txt")
