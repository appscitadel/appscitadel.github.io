"""One-off: rebrand build.py from appscitadel to the OFQ Ventures identity (colours, fonts, logo, email)."""
import re
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "build.py"
s = p.read_text(encoding="utf-8")

AR = "U+0600-06FF,U+0750-077F,U+0870-08FF,U+FB50-FDFF,U+FE70-FEFF"
LA = "U+0000-00FF,U+2000-206F"


def ff(family, file, weight, rng=None):
    r = f";unicode-range:{rng}" if rng else ""
    return f'@font-face{{font-family:"{family}";src:url("/assets/fonts/{file}.woff2") format("woff2");font-weight:{weight};font-display:swap{r}}}'


FONTS = "\n".join([
    ff("Alexandria", "alexandria-arabic-700-normal", 700, AR),
    ff("Alexandria", "alexandria-arabic-600-normal", 600, AR),
    ff("Alexandria", "alexandria-latin-700-normal", 700, LA),
    ff("Alexandria", "alexandria-latin-600-normal", 600, LA),
    ff("Plex Arabic", "ibm-plex-sans-arabic-arabic-400-normal", 400, AR),
    ff("Plex Arabic", "ibm-plex-sans-arabic-arabic-500-normal", 500, AR),
    ff("Plex Arabic", "ibm-plex-sans-arabic-arabic-600-normal", 600, AR),
    ff("Manrope", "manrope-latin-400-normal", 400),
    ff("Manrope", "manrope-latin-600-normal", "500 600"),
    ff("Manrope", "manrope-latin-700-normal", 700),
    ':root{--bg:#F5F1E8;--surface:#FBF9F4;--surface-2:#F1ECE2;--text:#171814;--muted:#5E6059;--line:#DDD4C5;'
    '--gold:#B77A19;--gold-ink:#8C5A10;--gold-soft:color-mix(in srgb,#B77A19 11%,transparent);--accent:#0F5C4A;'
    '--radius:8px;--shadow:0 1px 2px rgba(23,24,20,.04),0 10px 30px rgba(23,24,20,.05);'
    '--display:"Alexandria","Manrope","Plex Arabic",system-ui,sans-serif;--body:"Manrope","Plex Arabic",system-ui,sans-serif}',
    '@media (prefers-color-scheme:dark){:root{--bg:#181A16;--surface:#1F211C;--surface-2:#23251F;--text:#F1ECE2;'
    '--muted:#A8A699;--line:rgba(255,253,248,.13);--gold-ink:#D9A94C;--gold-soft:color-mix(in srgb,#B77A19 22%,transparent);--shadow:none}}',
])

s, n = re.subn(r'@font-face\{font-family:"Readex Pro".*?\n:root\{.*?\}\n@media \(prefers-color-scheme:dark\)\{:root\{.*?\}\}',
               lambda m: FONTS, s, count=1, flags=re.S)
assert n == 1, "token block not found"

REPS = {
    'font:400 16.5px/1.9 "Readex Pro",system-ui,-apple-system,"Segoe UI",Tahoma,sans-serif;': 'font:400 16.5px/1.95 var(--body);',
    'a{color:var(--ink);': 'a{color:var(--gold-ink);',
    '.mark{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#0F5C4A,#0A3F33);display:grid;place-items:center}':
        '.mark{width:30px;height:30px;display:block}.brand b{font-family:var(--display);font-weight:700;letter-spacing:.3px}',
    '.nav a:hover{background:var(--accent-soft);': '.nav a:hover{background:var(--gold-soft);',
    '.lang a.on{background:var(--accent);color:#fff}': '.lang a.on{background:var(--text);color:var(--bg)}',
    'h1{font-size:clamp(30px,4.2vw,42px);line-height:1.25;margin:0 0 12px;font-weight:700;letter-spacing:-.2px}':
        'h1{font-family:var(--display);font-size:clamp(30px,4.2vw,44px);line-height:1.3;margin:0 0 12px;font-weight:700}',
    'border-color:var(--accent);text-decoration:none}': 'border-color:var(--gold);text-decoration:none}',
    '.point svg{width:22px;height:22px;color:var(--ink);': '.point svg{width:22px;height:22px;color:var(--gold-ink);',
    'background:var(--accent-soft);color:var(--ink);display:grid;place-items:center;font-size:14px':
        'background:var(--gold-soft);color:var(--gold-ink);display:grid;place-items:center;font-size:14px;font-family:var(--display)',
    '.dev{background:var(--accent-soft);color:var(--ink)}': '.dev{background:var(--gold-soft);color:var(--gold-ink)}',
    'section.s li::marker{color:var(--ink)}': 'section.s li::marker{color:var(--gold)}',
    '.btn{display:inline-flex;align-items:center;gap:8px;background:var(--accent);color:#fff;':
        '.btn{display:inline-flex;align-items:center;gap:8px;background:var(--text);color:var(--bg);',
    'border-radius:12px;font-weight:500;font-size:15px}': 'border-radius:var(--radius);font-weight:600;font-size:15px}',
    '.summary h2{margin:0 0 14px;font-size:18px}': '.summary h2{margin:0 0 14px;font-size:18px;font-family:var(--display)}',
    'section.s h2{display:flex;align-items:center;gap:12px;margin:0 0 10px;font-size:19px;font-weight:600;line-height:1.5}':
        'section.s h2{display:flex;align-items:center;gap:12px;margin:0 0 10px;font-size:19px;font-weight:600;line-height:1.5;font-family:var(--display)}',
    'border-radius:14px;padding:16px}': 'border-radius:var(--radius);padding:16px}',
    'border-radius:12px;overflow:hidden}': 'border-radius:var(--radius);overflow:hidden}',
    'border-radius:16px;padding:16px;box-shadow': 'border-radius:var(--radius);padding:16px;box-shadow',
    '.card:hover{transform:translateY(-2px);border-color:color-mix(in srgb,var(--accent) 40%,var(--line))}':
        '.card:hover{transform:translateY(-2px);border-color:var(--gold)}',
    '.card .n{font-weight:600;': '.card .n{font-weight:600;font-family:var(--display);',
    '<link rel="preload" href="/assets/ReadexPro-Variable.ttf" as="font" type="font/ttf" crossorigin>':
        '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="/assets/favicon-32.png" sizes="32x32">'
        '<link rel="apple-touch-icon" href="/assets/favicon-180.png">'
        '<link rel="preload" href="/assets/fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2" as="font" type="font/woff2" crossorigin>',
    '<span class="mark">{MARK}</span>appscitadel</a>': '<img class="mark" src="/assets/ofq-mark-primary.svg" alt=""><b>OFQ Ventures</b></a>',
    'EMAIL = "info@appscitadel.com"': 'EMAIL = "info@ofqventures.com"',
    '© 2026 appscitadel — OFQ Labs. جميع الحقوق محفوظة.': '© 2026 OFQ Ventures. جميع الحقوق محفوظة.',
    '© 2026 appscitadel — OFQ Labs. All rights reserved.': '© 2026 OFQ Ventures. All rights reserved.',
    'من تطوير <b>appscitadel</b>': 'من تطوير <b>OFQ Ventures</b>',
    'is developed by <b>appscitadel</b>': 'is developed by <b>OFQ Ventures</b>',
    'من appscitadel")': 'من OFQ Ventures")',
    'by appscitadel")': 'by OFQ Ventures")',
    'head("appscitadel — تطبيقات وألعاب عربية", "ar", "#0F5C4A", "تطبيقات وألعاب عربية هادفة من appscitadel على Google Play")':
        'head("تطبيقات وألعاب OFQ Ventures", "ar", "#0F5C4A", "تطبيقات وألعاب عربية هادفة من OFQ Ventures على Google Play")',
    '<a href="/">التطبيقات</a><a href="mailto:{EMAIL}">تواصل</a>':
        '<a href="/">التطبيقات</a><a href="https://ofqventures.com">الاستوديو</a><a href="mailto:{EMAIL}">تواصل</a>',
    '<a href="/">Apps</a><a href="mailto:{EMAIL}">Contact</a>':
        '<a href="/">Apps</a><a href="https://ofqventures.com/en">Studio</a><a href="mailto:{EMAIL}">Contact</a>',
}
missing = [k for k in REPS if k not in s]
for k, v in REPS.items():
    s = s.replace(k, v)
p.write_text(s, encoding="utf-8")
print("missing:", missing)
