"""Renders the OFQ games & apps hub (/ and /en/) and the privacy index (/privacy/) from apps.json.

Called by build.py. CSS and JS are inlined from src/ so the first view needs no extra blocking requests.
"""
import json
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://apps.ofqventures.com"
EMAIL = "contact@ofqventures.com"
COMPANY = "https://ofqventures.com"

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="i-gp" viewBox="0 0 24 24"><path fill="#00D4FF" d="M3.6 2.1 13.1 12l-9.5 9.9c-.4-.3-.6-.8-.6-1.4V3.5c0-.6.2-1.1.6-1.4z"/><path fill="#00F076" d="M3.6 2.1c.4-.3 1-.4 1.6-.1l11.2 6.4-3.3 3.6z"/><path fill="#FF3A44" d="m3.6 21.9 9.5-9.9 3.3 3.6-11.2 6.4c-.6.3-1.2.2-1.6-.1z"/><path fill="#FFD400" d="m16.4 8.4 3.9 2.2c1.1.6 1.1 2.2 0 2.8l-3.9 2.2-3.3-3.6z"/></symbol>
<symbol id="i-as" viewBox="0 0 24 24"><path fill="currentColor" d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></symbol>
<symbol id="i-wb" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9.2"/><path d="M2.8 12h18.4M12 2.8c2.6 2.6 3.9 5.7 3.9 9.2s-1.3 6.6-3.9 9.2c-2.6-2.6-3.9-5.7-3.9-9.2s1.3-6.6 3.9-9.2z"/></g></symbol>
</defs></svg>"""

T = {
    "ar": dict(
        lang="ar", dir="rtl", path="/", other="/en/", other_label="English", other_name="English",
        title="ألعاب أفق: ألعاب عربية ممتعة | OFQ Ventures",
        desc="ألغاز وكلمات وتحديات ذكاء وكرة قدم بالعربي. اكتشف كل ألعاب وتطبيقات OFQ Ventures وحمّلها من Google Play و App Store.",
        eyebrow="OFQ Ventures", h1="ألعاب عربية ممتعة من أفق",
        sub="ألغاز وكلمات وتحديات ذكاء وكرة قدم، كلها بالعربي وكلها مجانية. اختار لعبتك الجاية وابدأ.",
        count=lambda n: f"{n} لعبة وتطبيق", free="مجانية",
        feat_h="اخترنا لك", all_h="ألعابنا", apps_h="تطبيقاتنا", chips_label="انتقل إلى تصنيف",
        gp=("متوفر على", "Google Play"), ap=("حمّله من", "App Store"), wb=("العب على", "الموقع"),
        soon="قريبًا على App Store", install="تثبيت", soon_short="قريبًا", aria_on="على", aria_site="الموقع",
        priv_h="سياسات الخصوصية", priv_p="لكل تطبيق سياسة خصوصية مستقلة، متاحة بالعربية والإنجليزية.", priv_btn="عرض سياسات الخصوصية",
        foot_co="موقع OFQ Ventures", skip="تخطَّ إلى المحتوى", close="إغلاق", logo_alt="شعار OFQ Ventures",
        pv_title="سياسات الخصوصية | OFQ Ventures", pv_h1="سياسات الخصوصية",
        pv_p="اختر التطبيق لتقرأ سياسة الخصوصية الخاصة به.", pv_back="كل ألعابنا", pv_ar="عربي", pv_en="English",
        pv_meta="سياسات الخصوصية لتطبيقات وألعاب OFQ Ventures.",
    ),
    "en": dict(
        lang="en", dir="ltr", path="/en/", other="/", other_label="العربية", other_name="العربية",
        title="OFQ Games: fun Arabic games | OFQ Ventures",
        desc="Arabic word games, riddles, brain teasers and football quizzes. Discover every OFQ Ventures game and app on Google Play and the App Store.",
        eyebrow="OFQ Ventures", h1="Fun Arabic games from OFQ",
        sub="Word games, riddles, brain teasers and football quizzes, all in Arabic and all free. Pick your next game and play.",
        count=lambda n: f"{n} games and apps", free="Free to play",
        feat_h="Our picks", all_h="Our games", apps_h="Our apps", chips_label="Jump to a category",
        gp=("Get it on", "Google Play"), ap=("Download on the", "App Store"), wb=("Play on the", "Web"),
        soon="Coming soon to the App Store", install="Install", soon_short="Soon", aria_on="on", aria_site="the web",
        priv_h="Privacy policies", priv_p="Every app has its own privacy policy, in Arabic and English.", priv_btn="View privacy policies",
        foot_co="OFQ Ventures website", skip="Skip to content", close="Close", logo_alt="OFQ Ventures logo",
        pv_title="Privacy policies | OFQ Ventures", pv_h1="Privacy policies",
        pv_p="Choose an app to read its privacy policy.", pv_back="All our games", pv_ar="Arabic", pv_en="English",
        pv_meta="Privacy policies for OFQ Ventures apps and games.",
    ),
}


def load():
    return json.loads((ROOT / "apps.json").read_text(encoding="utf8"))


def badge(kind, href, t, name, cls=""):
    cap, big = t[kind]
    word = "Google Play" if kind == "gp" else "App Store" if kind == "ap" else None
    label = f"{name} {t['aria_on']} {word}" if word else f"{name} {t['aria_on']} {t['aria_site']}"
    sym = {"gp": "i-gp", "ap": "i-as", "wb": "i-wb"}[kind]
    cls_ = {"gp": "gp", "ap": "as", "wb": "wb"}[kind]
    return (f'<a class="sb {cls_}" href="{e(href)}" rel="noopener">'
            f'<svg aria-hidden="true"><use href="#{sym}"/></svg><span><small>{e(cap)}</small><b>{e(big)}</b></span><i class="sr"> {e(name)}</i></a>')


def stores(a, t, name):
    out = []
    if a["play"]:
        out.append(badge("gp", a["play"], t, name))
    if a["appStore"]:
        out.append(badge("ap", a["appStore"], t, name))
    else:
        out.append(f'<span class="soon">{e(t["soon"])}</span>')
    if a["web"]:
        out.append(badge("wb", a["web"], t, name))
    return '<div class="stores">' + "".join(out) + "</div>"


def common_attrs(a, t, en):
    nm = a["nameEn"] if en else a["nameAr"]
    tg = a["taglineEn"] if en else a["taglineAr"]
    ds = a["descEn"] if en else a["descAr"]
    cat = a["categoryEn"] if en else a["category"]
    return nm, tg, ds, cat, (
        f'data-id="{e(a["id"])}" data-pkg="{e(a["package"])}" data-cat="{e(a["category"])}" '
        f'data-name="{e(nm)}" data-tag="{e(tg)}" data-desc="{e(ds)}" style="--a:{a["accent"]}"')


def icon(a, nm, cls="ic", eager=False, size=256):
    if not a["icon"]:
        return f'<span class="{cls}" aria-hidden="true"></span>'
    return (f'<img class="{cls}" src="/{a["icon"]}" width="{size}" height="{size}" alt="" '
            f'{"" if eager else "loading=\"lazy\" "}decoding="async">')


def feat_card(a, t, en, eager):
    nm, tg, ds, cat, attrs = common_attrs(a, t, en)
    return (f'<article class="fc rv" {attrs}><a class="hit" href="{e(a["play"])}">{icon(a, nm, eager=eager)}'
            f'<span><h3>{e(nm)}</h3><p class="tg">{e(tg)}</p></span></a><p class="ds">{e(ds)}</p>{stores(a, t, nm)}</article>')


def grid_card(a, t, en):
    nm, tg, ds, cat, attrs = common_attrs(a, t, en)
    pills = f'<a class="get gp" href="{e(a["play"])}" ">{e(t["install"])}<i class="sr"> {e(nm)}</i></a>'
    if a["appStore"]:
        pills += f'<a class="get as" href="{e(a["appStore"])}" ">{e(t["install"])}<i class="sr"> {e(nm)}</i></a>'
    else:
        pills += f'<span class="get sn">{e(t["soon_short"])}</span>'
    return (f'<article class="card rv" {attrs}><a class="hit" href="{e(a["play"])}">{icon(a, nm)}'
            f'<span class="tx"><h3>{e(nm)}</h3><p class="tg">{e(tg)}</p></span></a>{pills}'
            f'{stores(a, t, nm)}</article>')


def hub_page(lang, apps):
    t = T[lang]
    en = lang == "en"
    live = sorted((a for a in apps if a["live"]), key=lambda a: a["order"])
    feat = [a for a in live if a["featured"]]
    rest = [a for a in live if not a["featured"]]
    games = [a for a in rest if a["kind"] == "game"]
    tools_ = [a for a in rest if a["kind"] != "game"]
    cats = []
    for a in games:
        if a["category"] not in cats:
            cats.append(a["category"])
    catname = {a["category"]: a["categoryEn"] if en else a["category"] for a in games}
    chips = "".join(f'<a class="chip" href="#c{i}" data-grp="c{i}">{e(catname[c])}</a>' for i, c in enumerate(cats))
    groups = "".join(
        f'<div class="grp" id="c{i}"><h3 class="gh">{e(catname[c])}</h3><div class="grid">'
        + "".join(grid_card(a, t, en) for a in games if a["category"] == c) + "</div></div>"
        for i, c in enumerate(cats))
    apps_html = ('<section class="sec" id="apps" aria-labelledby="ah"><h2 id="ah">' + e(t["apps_h"]) + '</h2><div class="grid">'
                 + "".join(grid_card(a, t, en) for a in tools_) + "</div></section>") if tools_ else ""
    fan_ids = ["timoz", "sabakalemat", "negm", "fourpicword", "ehzerla3eb"]
    byid = {a["id"]: a for a in live}
    fan = "".join(icon(byid[i], "", cls="", eager=True, size=256).replace('width="256" height="256"', 'width="76" height="76"')
                  for i in fan_ids if i in byid)
    css = (ROOT / "src" / "hub.css").read_text(encoding="utf8")
    js = (ROOT / "src" / "hub.js").read_text(encoding="utf8")
    url = SITE + t["path"]
    other_url = SITE + t["other"]
    ar_url, en_url = SITE + "/", SITE + "/en/"
    fonts = ('<link rel="preload" href="/assets/fonts/manrope-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>'
             '<link rel="preload" href="/assets/fonts/alexandria-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>') if en else (
             '<link rel="preload" href="/assets/fonts/alexandria-arabic-700-normal.woff2" as="font" type="font/woff2" crossorigin>'
             '<link rel="preload" href="/assets/fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2" as="font" type="font/woff2" crossorigin>')
    boot = ("var h=document.documentElement,u=navigator.userAgent||'',p=/android/i.test(u)?'android':(/iPhone|iPad|iPod/i.test(u)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1))?'ios':'desktop';"
            "h.className+=' js '+p;var m=location.search.match(/[?&]lang=(\\w+)/);"
            f"if(m&&m[1]!=='{lang}'&&(m[1]==='en'||m[1]==='ar')){{location.replace((m[1]==='en'?'/en/':'/')+location.search.replace(/([?&])lang=\\w+&?/,'$1').replace(/[?&]$/,''))}}")
    return f"""<!doctype html>
<html lang="{t['lang']}" dir="{t['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<meta name="theme-color" content="#0F5C4A">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ar" href="{ar_url}"><link rel="alternate" hreflang="en" href="{en_url}"><link rel="alternate" hreflang="x-default" href="{ar_url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="OFQ Ventures">
<meta property="og:title" content="{e(t['title'])}"><meta property="og:description" content="{e(t['desc'])}">
<meta property="og:url" content="{url}"><meta property="og:locale" content="{'en_US' if en else 'ar_AR'}">
<meta property="og:image" content="{SITE}/assets/hub-og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(t['h1'])}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(t['title'])}">
<meta name="twitter:description" content="{e(t['desc'])}"><meta name="twitter:image" content="{SITE}/assets/hub-og.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/favicon-180.png">
{fonts}
<script>{boot}</script>
<style>{css}</style>
</head>
<body>
{SPRITE}
<a class="sr" href="#main">{e(t['skip'])}</a>
<div class="wrap">
<header class="top"><a class="brand" href="{COMPANY}"><img src="/assets/ofq-mark-primary.svg" width="32" height="32" alt="{e(t['logo_alt'])}"><span>OFQ Ventures</span></a>
<a class="lang" data-lang href="{t['other']}" hreflang="{'ar' if en else 'en'}" lang="{'ar' if en else 'en'}">{e(t['other_label'])}</a></header>
<main id="main">
<section class="hero" aria-labelledby="h1"><span class="eyebrow">{e(t['eyebrow'])}</span>
<h1 id="h1">{e(t['h1'])}</h1><p>{e(t['sub'])}</p>
<ul class="stats"><li>{e(t['count'](len(live)))}</li><li>{e(t['free'])}</li></ul>
<div class="fan" aria-hidden="true">{fan}</div></section>
<p class="note" id="now" role="status" hidden></p>
<section class="sec" aria-labelledby="fh"><h2 id="fh">{e(t['feat_h'])}</h2><div class="feat">{''.join(feat_card(a, t, en, True) for a in feat)}</div></section>
<section class="sec" aria-labelledby="gh"><h2 id="gh">{e(t['all_h'])}</h2>
<nav class="bar" aria-label="{e(t['chips_label'])}"><div class="chips">{chips}</div></nav>
{groups}</section>
{apps_html}
<section class="priv rv" aria-labelledby="ph"><h2 id="ph">{e(t['priv_h'])}</h2><p>{e(t['priv_p'])}</p><a class="btn" href="/privacy/{'en.html' if en else ''}">{e(t['priv_btn'])}</a></section>
</main>
<footer><div class="wrap"><a href="{COMPANY}{'/en' if en else ''}">{e(t['foot_co'])}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span class="sp"></span><a href="/privacy/{'en.html' if en else ''}">{e(t['priv_h'])}</a></div></footer>
</div>
<dialog id="sheet" aria-label="{e(t['h1'])}"><div id="sheet-body"></div></dialog>
<script>{js}</script>
</body>
</html>
"""


def privacy_index(lang, apps):
    t = T[lang]
    en = lang == "en"
    rows = []
    for a in sorted(apps, key=lambda a: a["order"]):
        nm = a["nameEn"] if en else a["nameAr"]
        rows.append(
            f'<li class="pr" style="--a:{a["accent"]}">{icon(a, nm, size=256).replace("class=\"ic\"", "class=\"ic s\"") if a["icon"] else ""}'
            f'<span class="pn">{e(nm)}</span><span class="pl"><a href="/privacy/{e(a["id"])}.html" lang="ar">{t["pv_ar"]}</a>'
            f'<a href="/privacy/{e(a["id"])}-en.html" lang="en">{t["pv_en"]}</a></span></li>')
    css = (ROOT / "src" / "hub.css").read_text(encoding="utf8")
    extra = (".pl{display:flex;gap:8px;margin-inline-start:auto}.pl a{display:inline-flex;align-items:center;min-height:48px;padding:0 16px;border-radius:999px;border:1px solid var(--line);background:var(--surface);font-weight:600;font-size:15px}"
             ".pr{display:flex;align-items:center;gap:12px;padding:10px 14px;border-radius:20px;background:var(--surface);border:1px solid var(--line);flex-wrap:wrap}"
             ".pr .ic.s{width:48px;height:48px}.pn{font-family:var(--display);font-weight:600;font-size:16px;flex:1 1 180px}"
             ".list{list-style:none;margin:20px 0 0;padding:0;display:grid;gap:10px}.back{display:inline-flex;align-items:center;min-height:48px;margin-top:8px;text-decoration:underline;text-decoration-color:var(--gold);text-underline-offset:4px}"
             "@media(min-width:800px){.list{grid-template-columns:1fr 1fr}}")
    # one page, two languages: the Arabic one at /privacy/ and the English one at /privacy/en.html
    return f"""<!doctype html>
<html lang="{t['lang']}" dir="{t['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(t['pv_title'])}</title>
<meta name="description" content="{e(t['pv_meta'])}">
<meta name="theme-color" content="#0F5C4A">
<link rel="canonical" href="{SITE}/privacy/{'en.html' if en else ''}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/favicon-180.png">
<link rel="preload" href="/assets/fonts/{'manrope-latin-400-normal' if en else 'ibm-plex-sans-arabic-arabic-400-normal'}.woff2" as="font" type="font/woff2" crossorigin>
<style>{css}{extra}</style>
</head>
<body>
<div class="wrap">
<header class="top"><a class="brand" href="/"><img src="/assets/ofq-mark-primary.svg" width="32" height="32" alt="{e(t['logo_alt'])}"><span>OFQ Ventures</span></a>
<a class="lang" href="{'/privacy/' if en else '/privacy/en.html'}" hreflang="{'ar' if en else 'en'}" lang="{'ar' if en else 'en'}">{e(t['other_label'])}</a></header>
<main id="main"><h1 style="font-family:var(--display);font-size:clamp(28px,6vw,44px);line-height:1.3;margin:24px 0 6px">{e(t['pv_h1'])}</h1>
<p style="margin:0;color:var(--muted)">{e(t['pv_p'])}</p>
<ul class="list">{''.join(rows)}</ul>
<a class="back" href="{'/en/' if en else '/'}">{e(t['pv_back'])}</a></main>
<footer><div class="wrap"><a href="{COMPANY}">{e(t['foot_co'])}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div></footer>
</div>
</body>
</html>
"""


def write_all(apps):
    (ROOT / "index.html").write_text(hub_page("ar", apps), encoding="utf8")
    (ROOT / "en").mkdir(exist_ok=True)
    (ROOT / "en" / "index.html").write_text(hub_page("en", apps), encoding="utf8")
    (ROOT / "privacy" / "index.html").write_text(privacy_index("ar", apps), encoding="utf8")
    (ROOT / "privacy" / "en.html").write_text(privacy_index("en", apps), encoding="utf8")
