"""Builds privacy pages and the /en/ redirect without writing index.html.

Run: python -X utf8 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
UPDATED_AR = "24 أكتوبر 2026"
UPDATED_EN = "October 24, 2026"
EMAIL = "contact@ofqventures.com"
DEV_URL = "https://play.google.com/store/apps/developer?id=OFQ+Labs"

import json
import hub

# One entry per product in apps.json. Privacy pages need every package (live or not) from the OFQ Labs account.
# Tuple: package, Arabic name, English name, accent, kind ("reader" | "game"), glyph shown in the policy badge
APPS = [(a["id"], a["nameAr"], a["nameEn"], a["accent"], "reader" if a["kind"] == "app" else "game", a["glyph"])
        for a in json.loads((ROOT / "apps.json").read_text(encoding="utf8")) if a["package"].startswith("com.appscitadel.")]

SUBSET_FONTS = (
    "ibm-plex-sans-arabic-arabic-400-normal", "ibm-plex-sans-arabic-arabic-600-normal",
    "alexandria-arabic-700-normal", "manrope-latin-400-normal",
    "manrope-latin-600-normal", "manrope-latin-700-normal",
)


def font_href(name):
    # Without optional build dependencies, use the original complete fonts.
    try:
        import fontTools
    except ImportError:
        return f"/assets/fonts/{name}.woff2"
    file = ROOT / "assets" / "fonts" / f"{name}-subset.woff2"
    return f"/assets/fonts/{name}-subset.woff2" if name in SUBSET_FONTS and file.is_file() else f"/assets/fonts/{name}.woff2"


def prepare_font_subsets():
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
    except ImportError:
        print("fontTools unavailable; using original complete fonts")
        return
    text = "".join((ROOT / name).read_text(encoding="utf8") for name in ("build.py", "hub.py", "apps.json"))
    unicodes = set(range(32, 127)) | set(range(0x600, 0x660)) | {ord(c) for c in text}
    for name in SUBSET_FONTS:
        font = TTFont(ROOT / "assets" / "fonts" / f"{name}.woff2", recalcTimestamp=False)
        options = subset.Options()
        options.flavor = "woff2"
        options.layout_features = ["*"]
        sub = subset.Subsetter(options=options)
        sub.populate(unicodes=unicodes)
        sub.subset(font)
        font.save(ROOT / "assets" / "fonts" / f"{name}-subset.woff2")


CSS = """
@font-face{font-family:OFQText;src:url('/assets/fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2') format('woff2');font-weight:400;font-display:swap;unicode-range:U+0600-06FF,U+0750-077F,U+0870-08FF,U+FB50-FDFF,U+FE70-FEFF}
@font-face{font-family:OFQText;src:url('/assets/fonts/ibm-plex-sans-arabic-arabic-600-normal.woff2') format('woff2');font-weight:600;font-display:swap;unicode-range:U+0600-06FF,U+0750-077F,U+0870-08FF,U+FB50-FDFF,U+FE70-FEFF}
@font-face{font-family:OFQText;src:url('/assets/fonts/manrope-latin-400-normal.woff2') format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:OFQText;src:url('/assets/fonts/manrope-latin-600-normal.woff2') format('woff2');font-weight:600;font-display:swap}
@font-face{font-family:OFQText;src:url('/assets/fonts/manrope-latin-700-normal.woff2') format('woff2');font-weight:700;font-display:swap}
@font-face{font-family:OFQDisplay;src:url('/assets/fonts/alexandria-arabic-600-normal.woff2') format('woff2');font-weight:600;font-display:swap;unicode-range:U+0600-06FF,U+0750-077F,U+0870-08FF,U+FB50-FDFF,U+FE70-FEFF}
@font-face{font-family:OFQDisplay;src:url('/assets/fonts/alexandria-arabic-700-normal.woff2') format('woff2');font-weight:700;font-display:swap;unicode-range:U+0600-06FF,U+0750-077F,U+0870-08FF,U+FB50-FDFF,U+FE70-FEFF}
@font-face{font-family:OFQDisplay;src:url('/assets/fonts/manrope-latin-700-normal.woff2') format('woff2');font-weight:700;font-display:swap}
:root{--green:#075844;--ink:#183d32;--text:#183d32;--muted:#53675b;--mint:#f0f5ec;--line:#dce5d7;--gold:#d1a541;--paper:#fffefb;--surface:#fff;--radius:16px;--text-xs:13px;--text-sm:15px;--text-base:16px;--text-lg:18px;--heading-sm:clamp(18px,1.5vw,21px);--heading-md:clamp(23px,2.5vw,32px);--heading-lg:clamp(28px,3.6vw,46px);--body:OFQText,Arial,sans-serif;--display:OFQDisplay,Arial,sans-serif}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:80px;-webkit-text-size-adjust:100%}body{margin:0;background:var(--paper);color:var(--ink);font:400 var(--text-base)/1.7 var(--body);font-synthesis:none;-webkit-font-smoothing:antialiased}a{color:var(--green);text-decoration:none;text-underline-offset:4px}a:hover{text-decoration:underline}a,summary{touch-action:manipulation;-webkit-tap-highlight-color:transparent}a:focus-visible,summary:focus-visible{outline:3px solid #a76f10;outline-offset:4px}img{display:block;max-width:100%}svg{flex:none}b,strong{font-weight:600}html[lang=en] b,html[lang=en] strong{font-weight:700}h1,h2,h3{font-family:var(--display);font-weight:600;line-height:1.5}html[lang=en] h1,html[lang=en] h2,html[lang=en] h3{font-weight:700;line-height:1.3}.wrap{width:min(1200px,calc(100% - 80px));margin-inline:auto}.skip{position:fixed;top:-100px;inset-inline-start:16px;padding:12px 20px;background:#fff;z-index:100}.skip:focus{top:0}
.topbar{position:sticky;top:0;z-index:30;background:#fffefbf5;border-bottom:1px solid var(--line);backdrop-filter:blur(14px)}.topbar>.wrap{height:60px;display:flex;align-items:center;justify-content:space-between;gap:24px}.brand{display:inline-flex;flex:none;align-items:center;direction:ltr;min-height:44px}.brand img{width:100px;height:36px;object-fit:contain}.nav{display:flex;align-items:center;gap:28px}.nav>a{min-height:44px;display:flex;align-items:center;font-size:15px;font-weight:600;color:var(--ink)}html[lang=en] .nav>a{font-weight:700}.nav-actions{display:flex;align-items:center;gap:8px}.language{display:inline-flex;justify-content:center;align-items:center;min-height:44px;border:1px solid var(--line);border-radius:30px;padding:8px 16px;font-size:13px;color:var(--ink);white-space:nowrap}.language:hover{background:var(--mint);text-decoration:none}.mobile-nav{display:none}.mobile-nav summary{display:grid;place-items:center;width:44px;height:44px;border:1px solid var(--line);border-radius:10px;list-style:none;cursor:pointer}.mobile-nav summary::-webkit-details-marker{display:none}.mobile-nav summary svg{width:21px;height:21px}.mobile-links{position:absolute;top:100%;inset-inline:0;padding:16px 18px;background:var(--paper);border-bottom:1px solid var(--line);box-shadow:0 12px 20px #183d3210;display:grid}.mobile-links a{display:flex;align-items:center;min-height:48px;padding:8px 12px;border-radius:8px;color:var(--ink)}.mobile-links a:hover{background:var(--mint)}
.hero{padding:44px 0 32px;max-width:calc(74ch + 246px);padding-inline-start:246px;margin-inline:auto}.app{display:flex;align-items:center;gap:14px;margin-bottom:24px;min-width:0}.badge{width:52px;height:52px;border-radius:14px;background:var(--accent,var(--green));color:white;display:grid;place-items:center;font-size:24px;font-weight:600;flex:none}.app .name{font-size:18px;font-weight:600;line-height:1.6}.app .pkg{font-size:13px;color:var(--muted);direction:ltr;text-align:start;unicode-bidi:plaintext;overflow-wrap:anywhere}h1{font-size:var(--heading-lg);font-weight:700;margin:0 0 14px}.lead{font-size:var(--text-lg);color:var(--muted);margin:0;max-width:70ch}.meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}.pill{font-size:13px;line-height:1.7;color:var(--muted);background:var(--mint);border:1px solid var(--line);padding:5px 12px;border-radius:999px}.grid{display:grid;grid-template-columns:210px minmax(0,74ch);gap:36px;align-items:start;justify-content:center;padding-bottom:64px}.grid>div{min-width:0}.toc{position:sticky;top:88px;font-size:15px;line-height:1.7}.toc .t{font-size:13px;font-weight:600;color:var(--muted);margin-bottom:10px}.toc ol{list-style:none;margin:0;padding:0;border-inline-start:2px solid var(--line)}.toc li a{display:flex;align-items:center;min-height:44px;padding:8px 14px;color:var(--muted);margin-inline-start:-2px;border-inline-start:2px solid transparent}.toc li a:hover{color:var(--green);border-color:var(--green);text-decoration:none}.summary{padding:24px;border:1px solid var(--line);border-radius:var(--radius);background:var(--mint);margin-bottom:32px}.summary h2{font-size:var(--heading-sm);margin:0 0 18px}.points{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.point svg{width:23px;height:23px;color:var(--green);margin-bottom:8px}.point b{display:block;font-size:16px;line-height:1.7}.point span{display:block;color:var(--muted);font-size:15px;line-height:1.7;margin-top:5px}section.s{padding:0 0 28px;margin-bottom:28px;border-bottom:1px solid var(--line);scroll-margin-top:84px}section.s:last-child{margin-bottom:0;border-bottom:0;padding-bottom:0}section.s h2{display:flex;align-items:flex-start;gap:12px;margin:0 0 16px;font-size:var(--heading-sm)}.num{flex:none;min-width:30px;height:30px;border-radius:8px;background:var(--mint);color:var(--green);display:grid;place-items:center;font:600 15px/1 var(--display)}html[lang=en] .num{font-weight:700}section.s p{margin:0 0 14px}section.s p:last-child{margin-bottom:0}section.s ul{margin:10px 0 0;padding-inline-start:23px}section.s li{margin:8px 0}section.s li::marker{color:var(--green)}section.s a:not(.btn){text-decoration:underline}section.s h3{font-size:18px;margin:24px 0 12px}.table{width:100%;table-layout:fixed;border-collapse:separate;border-spacing:0;margin-top:16px;font-size:15px;border:1px solid var(--line);border-radius:12px;overflow:hidden}.table th,.table td{padding:14px;text-align:start;vertical-align:top;border-bottom:1px solid var(--line);overflow-wrap:anywhere}.table th{background:var(--mint);font-size:13px;font-weight:600;color:var(--muted)}.table tr:last-child td{border-bottom:0}.tag{display:inline-block;font-size:13px;padding:3px 8px;border-radius:8px;line-height:1.7}.no{background:#edf6ed;color:#226234}.dev{background:#eef2ec;color:#31523c}.ads{background:#fff1dd;color:#80501a}.contact{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}.contact p{flex:1 1 240px}.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;background:var(--green);color:white;padding:10px 18px;border-radius:10px;font-size:15px;font-weight:600;max-width:100%;overflow-wrap:anywhere}.btn svg{flex:none}.btn:hover{background:#0c4435;text-decoration:none}html[lang=en] .btn,html[lang=en] .pn,html[lang=en] .app .name,html[lang=en] .toc .t,html[lang=en] .table th{font-weight:700}
footer{border-top:1px solid var(--line);background:var(--paper)}.footer-top{display:flex;align-items:center;flex-wrap:wrap;gap:30px;padding-block:28px}.footer-top>.brand{margin:0}.footer-top>a:nth-child(2){margin-inline-start:auto}.footer-top>a:not(.brand){display:flex;align-items:center;min-height:44px;font-size:15px}.footer-bottom>a{display:inline-flex;align-items:center;min-height:44px}.footer-bottom{align-items:center;display:flex;justify-content:space-between;gap:16px;border-top:1px solid var(--line);padding-block:20px;font-size:13px;color:var(--muted)}
.privacy-index{padding-block:44px 64px}.privacy-index>p{margin:0;color:var(--muted);font-size:18px;max-width:65ch}.list{list-style:none;margin:28px 0 24px;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.pr{display:flex;align-items:center;flex-wrap:wrap;gap:14px;padding:20px;border-radius:var(--radius);border:1px solid var(--line);background:#fff;min-width:0}.pr .ic{width:48px;height:48px;object-fit:contain;border-radius:12px;flex:none}.pn{flex:1 1 150px;font-size:16px;font-weight:600;line-height:1.7}.pl{display:flex;gap:8px;margin-inline-start:auto}.pl a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:8px 14px;border:1px solid var(--line);border-radius:999px;font-size:15px}.pl a:hover{background:var(--mint);text-decoration:none}.back{display:inline-flex;align-items:center;min-height:44px;text-decoration:underline;font-size:15px}
@media(max-width:1000px){.hero{max-width:calc(74ch + 208px);padding-inline-start:208px}.grid{grid-template-columns:180px minmax(0,1fr);gap:28px}.nav{gap:20px}.points{grid-template-columns:1fr}.point{display:grid;grid-template-columns:24px 1fr;column-gap:12px}.point svg{grid-row:1/3;margin-top:2px}.point span{grid-column:2}.point b{grid-column:2}}
@media(max-width:860px){.wrap{width:calc(100% - 48px)}.nav{display:none}.mobile-nav{display:block}.grid{grid-template-columns:minmax(0,74ch)}.toc{display:none}.list{grid-template-columns:1fr}.hero{max-width:none;padding-inline-start:0;margin-inline:0}.table th,.table td{padding:12px}}
@media(max-width:600px){.wrap{width:calc(100% - 36px)}.topbar>.wrap{height:56px;gap:12px}.topbar .brand img{width:89px;height:32px}.hero{padding-top:30px;padding-bottom:28px}.app{gap:12px;margin-bottom:22px}.badge{width:48px;height:48px}.app .name{font-size:16px}.lead{font-size:16px}.grid{padding-bottom:44px}.summary{padding:20px;margin-bottom:28px}.points{gap:18px}section.s{padding-bottom:24px;margin-bottom:24px}.table thead{display:none}.table,.table tbody,.table tr,.table td{display:block;width:100%}.table tr{padding:14px;border-bottom:1px solid var(--line)}.table tr:last-child{border-bottom:0}.table td{border:0;padding:4px 0}.table td:first-child{font-weight:600}.table td:nth-child(2){margin-block:3px}.contact .btn{width:100%;font-size:15px}.footer-top{padding-block:24px;gap:8px 20px}.footer-top>.brand{width:100%;margin-bottom:6px}.footer-top>a:nth-child(2){margin:0}.footer-bottom{flex-direction:column;gap:8px}.privacy-index{padding-block:30px 44px}.privacy-index>p{font-size:16px}.pr{padding:18px;gap:12px}.pn{flex-basis:calc(100% - 60px)}.pl{width:100%;margin:0}.pl a{flex:1}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
/* Pass 3: current OFQ palette and shared contact/footer composition. */
:root{--green:#8c5a10;--ink:#171814;--muted:#5e6059;--mint:#eee8dd;--line:#ddd4c5;--paper:#fbf9f4;--radius:20px;--shadow:0 18px 44px #17181412}
body{background:var(--paper)}bdi{unicode-bidi:isolate}.hero{border-bottom:1px solid var(--line);margin-bottom:32px;padding-bottom:32px}.app .badge{border-radius:12px}.summary{background:#f5f1e8;padding:28px}.toc ol{border-color:var(--line)}.toc li a:hover{color:var(--green);border-color:var(--green)}.btn{background:var(--green);border-radius:10px}.btn:hover{background:#734a0d}.contact-extra{display:flex;align-items:center;gap:24px;flex-wrap:wrap;margin-top:16px}.contact-extra a{min-height:44px;display:inline-flex;align-items:center;font-size:15px;font-weight:600}.pr{background:#fffdf8;border-radius:16px}.list{gap:14px}.pr:hover{border-color:#c8bda9}.privacy-index>h1{margin-bottom:18px}.privacy-index>p{max-width:65ch}.topbar{background:var(--paper)}
footer{background:#f5f1e8}.footer-top{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:40px;padding-block:40px}.footer-brand p{font-size:16px;color:var(--muted);margin:16px 0 0}.footer-contact,.footer-nav{display:grid;align-content:start}.footer-contact a,.footer-nav a{display:flex;align-items:center;min-height:44px;font-size:15px;width:fit-content;max-width:100%;overflow-wrap:anywhere}.footer-bottom{padding-block:22px;align-items:center}.footer-top a:hover{color:var(--green)}
@media(max-width:860px){.footer-top{grid-template-columns:1fr 1fr;gap:24px}.footer-brand{grid-column:1/-1}}
@media(max-width:600px){.hero{padding-top:30px;padding-bottom:28px;margin-bottom:24px}.summary{padding:22px}.footer-top{grid-template-columns:1fr;gap:22px;padding-block:30px}.footer-brand{grid-column:auto}.footer-brand p{margin-top:10px}.footer-bottom{align-items:start}.contact-extra{gap:8px 20px}.contact-extra a{font-size:15px}}

"""

MARK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F3E2B5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 15.4 6.8 18.1l1-5.8L3.5 8.2l5.9-.9z"/></svg>'
ICON_LOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M11 18h2"/></svg>'
ICON_SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6z"/><path d="M9 12l2 2 4-4"/></svg>'
ICON_MAIL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 6.5L12 13l8.5-6.5"/></svg>'


def head(title, lang, accent, desc):
    d = "rtl" if lang == "ar" else "ltr"
    font = "ibm-plex-sans-arabic-arabic-400-normal" if lang == "ar" else "manrope-latin-400-normal"
    heading_font = "alexandria-arabic-700-normal" if lang == "ar" else "manrope-latin-700-normal"
    return f"""<!doctype html><html lang="{lang}" dir="{d}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f5f1e8">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="/assets/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="/assets/favicon-180.png">
<link rel="preload" href="{font_href(font)}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{font_href(heading_font)}" as="font" type="font/woff2" crossorigin>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"OFQ Ventures","url":"https://ofqventures.com","email":"contact@ofqventures.com","telephone":"+201500002663"}}</script><link rel="stylesheet" href="/assets/site.css"><style>:root{{--accent:{accent}}}</style></head><body>"""


def topbar(lang, other_href):
    en = lang == "en"
    home = "/?lang=en" if en else "/?lang=ar"
    labels = ("Services", "Products", "About OFQ", "Contact") if en else ("خدماتنا", "منتجاتنا", "عن أفق", "تواصل معنا")
    nav = "".join(f'<a href="{home}#{anchor}">{label}</a>' for anchor, label in zip(("services", "games", "about"), labels))
    nav += f'<a href="{home}#contact">{labels[3]}</a>'
    switch = "العربية" if en else "English"
    other = "ar" if en else "en"
    menu = "Open menu" if en else "فتح القائمة"
    skip = "Skip to content" if en else "تخطَّ إلى المحتوى"
    return f"""<a class="skip" href="#intro">{skip}</a><header class="topbar"><div class="wrap">
<a class="brand" href="{home}" aria-label="OFQ Ventures"><img src="/assets/ofq-lockup.svg" width="100" height="36" alt="OFQ Ventures"></a>
<nav class="nav" aria-label="{'Main navigation' if en else 'القائمة الرئيسية'}">{nav}</nav>
<div class="nav-actions"><a class="language" href="{other_href}" hreflang="{other}" lang="{other}">{switch}</a>
<details class="mobile-nav"><summary aria-label="{menu}"><svg aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></summary><nav class="mobile-links" aria-label="{menu}">{nav}</nav></details></div>
</div></header>"""


def footer(lang):
    en = lang == "en"
    home = "/?lang=en" if en else "/?lang=ar"
    policies = "/privacy/en.html" if en else "/privacy/"
    rights = "All rights reserved." if en else "جميع الحقوق محفوظة."
    label = "Privacy policies" if en else "سياسات الخصوصية"
    company = "OFQ Ventures website" if en else "موقع OFQ Ventures"
    products = "Products" if en else "منتجاتنا"
    wa = "Chat on WhatsApp" if en else "تواصل على واتساب"
    return f'<footer><div class="wrap footer-top"><div class="footer-brand"><a class="brand" href="{home}" aria-label="OFQ Ventures"><img src="/assets/ofq-lockup.svg" width="100" height="36" alt="OFQ Ventures" loading="lazy" decoding="async"></a><p>{"Software and products by OFQ" if en else "برمجيات ومنتجات من أفق"}</p></div><div class="footer-contact"><a href="mailto:{EMAIL}"><bdi dir="ltr">{EMAIL}</bdi></a><a href="tel:+201500002663"><bdi dir="ltr">+20 150 000 2663</bdi></a><a href="https://wa.me/201500002663">{wa}</a></div><div class="footer-nav"><a href="{home}#games">{products}</a><a href="{policies}">{label}</a><a href="https://ofqventures.com{"/en" if en else ""}">{company}</a></div></div><div class="wrap footer-bottom"><span>© 2026 OFQ Ventures. {rights}</span><span>Android · Web</span></div></footer></body></html>'



def stored_on_device(kind, lang):
    if lang == "ar":
        return "المفضلة وآخر فتوى قرأتها وإعدادات القراءة (حجم الخط والمظهر)" if kind == "reader" else "تقدّمك في المراحل والنقاط والإعدادات (الصوت والمظهر)"
    return "favourites, last read item and reading settings (font size, theme)" if kind == "reader" else "level progress, points and settings (sound, theme)"


def privacy_ar(pkg, name, accent, kind, glyph):
    secs = [
        ("intro", "من نحن ونطاق السياسة", f"<p>تطبيق «{name}» من تطوير <b><a href='https://ofqventures.com'>OFQ Ventures</a></b> (حساب المطوّر OFQ Labs على Google Play). توضّح هذه السياسة ما يحدث للبيانات عند استخدامك للتطبيق، وتنطبق على التطبيق فقط وليس على مواقع أو خدمات أطراف أخرى.</p>"),
        ("data", "البيانات التي يتعامل معها التطبيق", f"""<p>لا يتطلب التطبيق تسجيل حساب، ولا يطلب منك أي معلومات شخصية.</p>
<table class="table"><thead><tr><th>نوع البيانات</th><th>الحالة</th><th>التفاصيل</th></tr></thead><tbody>
<tr><td>الاسم، البريد، رقم الهاتف</td><td><span class="tag no">لا تُجمع</span></td><td>لا يوجد تسجيل دخول أو نماذج.</td></tr>
<tr><td>الموقع الجغرافي الدقيق، جهات الاتصال، الصور، الملفات</td><td><span class="tag no">لا تُجمع</span></td><td>لا يطلب التطبيق أي صلاحية للوصول إليها.</td></tr>
<tr><td>{stored_on_device(kind, 'ar')}</td><td><span class="tag dev">على جهازك فقط</span></td><td>تُحفظ محليًا ولا تُرسل إلينا، وتُحذف بحذف التطبيق.</td></tr>
<tr><td>معرّف الإعلانات، عنوان IP، بيانات التفاعل مع الإعلانات</td><td><span class="tag ads">عبر Google AdMob</span></td><td>لعرض الإعلانات وقياسها ومنع الاحتيال. انظر القسم التالي.</td></tr>
</tbody></table>"""),
        ("ads", "الإعلانات وملفات التعريف", """<p>يعرض التطبيق إعلانات من خلال <b>Google AdMob</b>، وهي الطريقة التي تبقي التطبيق مجانيًا. قد تستخدم Google وشركاؤها معرّف الإعلانات في جهازك وبيانات تقنية عامة لعرض إعلانات مناسبة وقياس أدائها.</p>
<ul><li>في الدول التي تشترط ذلك (مثل الاتحاد الأوروبي والمملكة المتحدة) يظهر لك نموذج موافقة من Google قبل عرض أي إعلان مخصص.</li>
<li>يمكنك تغيير اختيارك في أي وقت من إعدادات التطبيق ← «خيارات خصوصية الإعلانات».</li>
<li>للمزيد: <a href="https://policies.google.com/technologies/partner-sites?hl=ar">كيف تستخدم Google البيانات من التطبيقات الشريكة</a>.</li></ul>"""),
        ("rights", "حقوقك وخياراتك", """<ul><li>إيقاف الإعلانات المخصّصة أو إعادة ضبط معرّف الإعلانات من: إعدادات أندرويد ← Google ← الإعلانات.</li>
<li>حذف كل بيانات التطبيق من جهازك بحذف التطبيق أو مسح بياناته من إعدادات أندرويد.</li>
<li>لأي طلب يتعلق ببياناتك راسلنا وسنرد خلال 30 يومًا.</li></ul>"""),
        ("kids", "خصوصية الأطفال", "<p>التطبيق غير موجّه للأطفال دون 13 عامًا، ولا نجمع عن علم أي بيانات منهم. إذا اعتقدت أن طفلًا قدّم بيانات، تواصل معنا وسنتعامل مع الأمر فورًا.</p>"),
        ("security", "الأمان ومدة الاحتفاظ", "<p>لا نشغّل خوادم تخزّن بيانات المستخدمين، لذلك لا نحتفظ بأي بيانات عنك. البيانات المحلية تبقى في مساحة التطبيق الخاصة على جهازك ويحميها نظام أندرويد.</p>"),
        ("changes", "التغييرات على هذه السياسة", "<p>قد نحدّث هذه السياسة عند تغيّر التطبيق أو المتطلبات القانونية. يظهر تاريخ آخر تحديث أعلى الصفحة، وأي تغيير جوهري سيُشار إليه داخل التطبيق.</p>"),
    ]
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t, _ in secs) + '<li><a href="#contact">التواصل</a></li>'
    body = "".join(f'<section class="s" id="{i}"><h2><span class="num">{n}</span>{t}</h2>{c}</section>' for n, (i, t, c) in enumerate(secs, 1))
    return (head(f"سياسة الخصوصية — {name}", "ar", accent, f"سياسة الخصوصية لتطبيق {name} من OFQ Ventures")
            + topbar("ar", f"{pkg}-en.html")
            + f"""<main class="wrap"><div class="hero"><div class="app"><span class="badge">{glyph}</span><div><div class="name">{name}</div><div class="pkg">com.appscitadel.{pkg}</div></div></div>
<h1>سياسة الخصوصية</h1><p class="lead">نحترم خصوصيتك. صُمّم التطبيق ليعمل دون أن يعرف عنك شيئًا، وهنا نشرح ذلك بوضوح ودون تعقيد.</p>
<div class="meta"><span class="pill">آخر تحديث: {UPDATED_AR}</span><span class="pill">يسري على Android</span></div></div>
<div class="grid"><aside class="toc"><div class="t">المحتويات</div><ol>{toc}</ol></aside><div>
<div class="summary"><h2>باختصار</h2><div class="points">
<div class="point">{ICON_LOCK}<b>لا نجمع بيانات شخصية</b><span>بدون حساب، بدون نماذج، بدون صلاحيات حساسة.</span></div>
<div class="point">{ICON_PHONE}<b>بياناتك على جهازك</b><span>تقدّمك وإعداداتك محفوظة محليًا فقط.</span></div>
<div class="point">{ICON_SHIELD}<b>إعلانات Google بموافقتك</b><span>نموذج موافقة حيث يلزم، وتقدر تغيّره أي وقت.</span></div>
</div></div>{body}
<section class="s" id="contact"><h2><span class="num">{len(secs)+1}</span>التواصل</h2><div class="contact"><p>لأي سؤال أو طلب بخصوص الخصوصية يسعدنا تواصلك.</p><a class="btn" href="mailto:{EMAIL}?subject={name}">{ICON_MAIL}{EMAIL}</a></div><div class="contact-extra" data-contact-chrome><a href="tel:+201500002663"><bdi dir="ltr">+20 150 000 2663</bdi></a><a href="https://wa.me/201500002663">تواصل على واتساب</a></div></section>
</div></div></main>""" + footer("ar"))


def privacy_en(pkg, name_ar, name, accent, kind, glyph):
    secs = [
        ("intro", "Who we are and scope", f"<p>{name} ({name_ar}) is developed by <b><a href='https://ofqventures.com/en'>OFQ Ventures</a></b> (developer account OFQ Labs on Google Play). This policy explains what happens to data when you use the app. It covers this app only, not third-party sites or services.</p>"),
        ("data", "Data the app handles", f"""<p>The app does not require an account and never asks for personal information.</p>
<table class="table"><thead><tr><th>Data type</th><th>Status</th><th>Details</th></tr></thead><tbody>
<tr><td>Name, email, phone number</td><td><span class="tag no">Not collected</span></td><td>No sign-in and no forms.</td></tr>
<tr><td>Precise location, contacts, photos, files</td><td><span class="tag no">Not collected</span></td><td>The app requests no permission to access them.</td></tr>
<tr><td>{stored_on_device(kind, 'en').capitalize()}</td><td><span class="tag dev">On your device only</span></td><td>Stored locally, never sent to us, removed when you uninstall.</td></tr>
<tr><td>Advertising ID, IP address, ad interaction data</td><td><span class="tag ads">Via Google AdMob</span></td><td>To serve and measure ads and prevent fraud. See the next section.</td></tr>
</tbody></table>"""),
        ("ads", "Advertising", """<p>The app shows ads through <b>Google AdMob</b>, which keeps it free. Google and its partners may use your device's advertising ID and general technical data to serve relevant ads and measure their performance.</p>
<ul><li>Where required (e.g. EEA and UK), Google's consent form is shown before any personalised ad.</li>
<li>You can change your choice at any time in the app's Settings → "Ad privacy options".</li>
<li>Learn more: <a href="https://policies.google.com/technologies/partner-sites">How Google uses information from partner apps</a>.</li></ul>"""),
        ("rights", "Your rights and choices", """<ul><li>Opt out of personalised ads or reset your advertising ID in Android Settings → Google → Ads.</li>
<li>Delete all app data by uninstalling the app or clearing its storage in Android settings.</li>
<li>Email us with any data request and we will respond within 30 days.</li></ul>"""),
        ("kids", "Children's privacy", "<p>The app is not directed to children under 13 and we do not knowingly collect data from them. If you believe a child has provided data, contact us and we will act promptly.</p>"),
        ("security", "Security and retention", "<p>We do not operate servers that store user data, so we retain nothing about you. Local data stays in the app's private storage, protected by Android.</p>"),
        ("changes", "Changes to this policy", "<p>We may update this policy when the app or legal requirements change. The last-updated date appears at the top, and material changes will be noted in the app.</p>"),
    ]
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t, _ in secs) + '<li><a href="#contact">Contact</a></li>'
    body = "".join(f'<section class="s" id="{i}"><h2><span class="num">{n}</span>{t}</h2>{c}</section>' for n, (i, t, c) in enumerate(secs, 1))
    return (head(f"Privacy Policy — {name}", "en", accent, f"Privacy policy for {name} by OFQ Ventures")
            + topbar("en", f"{pkg}.html")
            + f"""<main class="wrap"><div class="hero"><div class="app"><span class="badge">{glyph}</span><div><div class="name">{name}</div><div class="pkg">com.appscitadel.{pkg}</div></div></div>
<h1>Privacy Policy</h1><p class="lead">We respect your privacy. The app is designed to work without knowing anything about you, and this page explains that plainly.</p>
<div class="meta"><span class="pill">Last updated: {UPDATED_EN}</span><span class="pill">Applies to Android</span></div></div>
<div class="grid"><aside class="toc"><div class="t">CONTENTS</div><ol>{toc}</ol></aside><div>
<div class="summary"><h2>In short</h2><div class="points">
<div class="point">{ICON_LOCK}<b>No personal data collected</b><span>No account, no forms, no sensitive permissions.</span></div>
<div class="point">{ICON_PHONE}<b>Your data stays on your device</b><span>Progress and settings are stored locally only.</span></div>
<div class="point">{ICON_SHIELD}<b>Google ads, with your consent</b><span>Consent form where required, changeable anytime.</span></div>
</div></div>{body}
<section class="s" id="contact"><h2><span class="num">{len(secs)+1}</span>Contact</h2><div class="contact"><p>Questions or requests about privacy? We're happy to help.</p><a class="btn" href="mailto:{EMAIL}?subject={name}">{ICON_MAIL}{EMAIL}</a></div><div class="contact-extra" data-contact-chrome><a href="tel:+201500002663"><bdi dir="ltr">+20 150 000 2663</bdi></a><a href="https://wa.me/201500002663">Chat on WhatsApp</a></div></section>
</div></div></main>""" + footer("en"))


def ext(html):
    """External links open in a new tab."""
    return html.replace('<a href="http', '<a target="_blank" rel="noopener" href="http').replace("<a href='http", "<a target='_blank' rel='noopener' href='http").replace('<a class="btn ghost" href="http', '<a class="btn ghost" target="_blank" rel="noopener" href="http').replace('<a class="btn" href="http', '<a class="btn" target="_blank" rel="noopener" href="http')


def privacy_icons(apps):
    """Optional Pillow optimization; policies still build without extra dependencies.

    App originals stay untouched. The privacy index uses these small responsive
    WebPs when available and otherwise falls back to the original app icon.
    """
    try:
        from PIL import Image
    except ImportError:
        print("Pillow not installed: privacy index uses original app icons")
        return
    out = ROOT / "privacy" / "icons"
    out.mkdir(parents=True, exist_ok=True)
    for app in apps:
        if not app["package"].startswith("com.appscitadel.") or not app["icon"]:
            continue
        source = ROOT / app["icon"]
        if not source.is_file():
            continue
        with Image.open(source) as original:
            original.load()
            for size in (96, 192):
                image = original.convert("RGBA")
                image.thumbnail((size, size), Image.Resampling.LANCZOS)
                image.save(out / f"{app['id']}-{size}.webp", "WEBP", quality=80, method=6)


def main():
    privacy_icons(json.loads((ROOT / "apps.json").read_text(encoding="utf8")))
    prepare_font_subsets()
    css = CSS
    for name in SUBSET_FONTS:
        css = css.replace(f"/assets/fonts/{name}.woff2", font_href(name))
    (ROOT / "assets" / "site.css").write_text(css.strip(), encoding="utf-8")
    out = ROOT / "privacy"
    out.mkdir(exist_ok=True)
    for p, n, e, a, k, g in APPS:
        (out / f"{p}.html").write_text(ext(privacy_ar(p, n, a, k, g)), encoding="utf-8")
        (out / f"{p}-en.html").write_text(ext(privacy_en(p, n, e, a, k, g)), encoding="utf-8")
    hub.write_all(json.loads((ROOT / "apps.json").read_text(encoding="utf8")))
    print(f"built {len(APPS)} apps x 2 languages + privacy indexes + /en/ redirect; index.html untouched")


if __name__ == "__main__":
    main()
