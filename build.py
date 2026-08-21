#!/usr/bin/env python3
"""Build: minify styles.css -> styles.min.css, inline it into all 6 pages.
Run after any styles.css edit: python3 build.py (or ./build.sh)."""
import re, subprocess, pathlib
root=pathlib.Path(__file__).parent
subprocess.run(['npx','--yes','csso-cli','styles.css','-o','styles.min.css'],cwd=root,check=True)
css=(root/'styles.min.css').read_text()
css=css.replace('url(assets/','url(/assets/').replace('url("assets/','url("/assets/')
tag='<style id="site-css">'+css+'</style>'
for p in ['index.html','services.html','roadmap.html','lt/index.html','lt/services.html','lt/roadmap.html']:
    f=root/p; h=f.read_text()
    h2,n=re.subn(r'<style id="site-css">.*?</style>', lambda m: tag, h, flags=re.S)
    if not n:
        h2,n=re.subn(r'<link rel="stylesheet" href="(?:\.\./)?styles\.min\.css\?v=\d+" />', tag, h)
    assert n==1, p
    f.write_text(h2)
    print('inlined', p)
