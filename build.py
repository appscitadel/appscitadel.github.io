"""Builds the appscitadel developer site: index.html + privacy/<package>.html.

Run: python -X utf8 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
UPDATED_AR = "20 أكتوبر 2026"
UPDATED_EN = "October 20, 2026"
EMAIL = "info@appscitadel.com"
DEV_URL = "https://play.google.com/store/apps/dev?id=4751617247366509411"

# package, Arabic name, English name, accent, kind ("reader" | "game"), glyph shown in the app badge
APPS = [
    ("fatawyibnbaz", "فتاوى ابن باز", "Fatawa Ibn Baz", "#0F5C4A", "reader", "ف"),
    ("wasla1", "وصلة التحدي - كلمات متقاطعة", "Wasla Challenge - Crosswords", "#C2410C", "game", "و"),
    ("sabakalemat", "سبع كلمات", "Seven Words", "#7C3AED", "game", "٧"),
    ("asharkalemat", "عشر كلمات", "Ten Words", "#2563EB", "game", "١٠"),
    ("hangman1", "حبل المشنقة - لعبة كلمات", "Hangman - Word Game", "#B45309", "game", "ح"),
    ("fourpicword", "أربع صور وكلمة", "4 Pics 1 Word", "#DB2777", "game", "٤"),
    ("logzweklma2", "لغز وكلمة - وصلة كلمات", "Riddle & Word - Word Link", "#0E7490", "game", "ل"),
    ("abaqeragame", "تحدي العباقرة - ألغاز", "Geniuses Challenge - Riddles", "#6D28D9", "game", "ع"),
    ("negm", "نجم - لعبة الذكاء والتسلية", "Negm - Brain Game", "#CA8A04", "game", "★"),
    ("logzweklma1", "لغز وكلمة - كلمات متقاطعة", "Riddle & Word - Crosswords", "#0F766E", "game", "ل"),
    ("sorteen_weklma", "صورتين وكلمة", "2 Pics 1 Word", "#BE185D", "game", "٢"),
    ("linkit", "احزر الكلمة - وصلة التحدي", "Guess the Word - Link It", "#EA580C", "game", "؟"),
    ("mathpuzzle", "تحدي الحساب", "Math Puzzle", "#1D4ED8", "game", "∑"),
    ("ehzerla3eb", "احزر اللاعب - أربع صور لاعب", "Guess the Player - 4 Pics", "#15803D", "game", "⚽"),
    ("ehzerla3eb2", "لعبة احزر اللاعب", "Guess the Player", "#166534", "game", "⚽"),
    ("fourpicword2", "أربع صور وكلمة - فطحل الألغاز", "4 Pics 1 Word - Riddle Master", "#9D174D", "game", "٤"),
    ("waslatahady", "وصلة التحدي", "Wasla Challenge", "#9A3412", "game", "و"),
]

CSS = """
@font-face{font-family:"Readex Pro";src:url("/assets/ReadexPro-Variable.ttf") format("truetype");font-weight:160 700;font-display:swap}
:root{--bg:#F6F4EF;--surface:#FFFFFF;--surface-2:#FAF8F3;--text:#1C2420;--muted:#5C6762;--line:#E6E1D6;--accent:#0F5C4A;--accent-soft:color-mix(in srgb,var(--accent) 9%,transparent);--ink:var(--accent);--radius:18px;--shadow:0 1px 2px rgba(28,36,32,.04),0 8px 28px rgba(28,36,32,.06)}
@media (prefers-color-scheme:dark){:root{--bg:#0F1412;--surface:#161D1A;--surface-2:#1B2420;--text:#E7ECE9;--muted:#9AA6A0;--line:#26302B;--accent-soft:color-mix(in srgb,var(--accent) 26%,transparent);--ink:color-mix(in srgb,var(--accent) 45%,#ffffff);--shadow:none}}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:400 16.5px/1.9 "Readex Pro",system-ui,-apple-system,"Segoe UI",Tahoma,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--ink);text-decoration:none;text-underline-offset:3px}a:hover{text-decoration:underline}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
.topbar{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}
.topbar .wrap{display:flex;align-items:center;justify-content:space-between;height:64px}
.brand{display:flex;align-items:center;gap:10px;color:var(--text);font-weight:600;letter-spacing:.2px}.brand:hover{text-decoration:none}
.mark{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#0F5C4A,#0A3F33);display:grid;place-items:center}
.nav{display:flex;gap:6px}.nav a{color:var(--muted);font-size:14.5px;padding:7px 12px;border-radius:999px}.nav a:hover{background:var(--accent-soft);color:var(--text);text-decoration:none}
.hero{padding:56px 0 28px}
.app{display:flex;align-items:center;gap:16px;margin-bottom:22px}
.badge{width:60px;height:60px;border-radius:16px;background:var(--accent);color:#fff;display:grid;place-items:center;font-size:26px;font-weight:600;box-shadow:0 8px 24px color-mix(in srgb,var(--accent) 35%,transparent)}
.app .name{font-weight:600;font-size:18px;line-height:1.4}.app .pkg{color:var(--muted);font-size:13.5px;direction:ltr;text-align:start;unicode-bidi:plaintext}
h1{font-size:clamp(30px,4.2vw,42px);line-height:1.25;margin:0 0 12px;font-weight:700;letter-spacing:-.2px}
.lead{color:var(--muted);font-size:17.5px;max-width:680px;margin:0}
.meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.pill{font-size:13.5px;color:var(--muted);background:var(--surface);border:1px solid var(--line);padding:5px 12px;border-radius:999px}
.lang{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:3px;background:var(--surface)}
.lang a{font-size:13.5px;padding:5px 14px;border-radius:999px;color:var(--muted)}.lang a.on{background:var(--accent);color:#fff}.lang a:hover{text-decoration:none}
.grid{display:grid;grid-template-columns:240px 1fr;gap:40px;align-items:start;padding-bottom:72px}
.toc{position:sticky;top:88px;font-size:14.5px}
.toc .t{font-size:12.5px;font-weight:600;color:var(--muted);letter-spacing:.4px;margin-bottom:10px}
.toc ol{list-style:none;margin:0;padding:0;border-inline-start:2px solid var(--line)}
.toc li a{display:block;padding:6px 14px;color:var(--muted);margin-inline-start:-2px;border-inline-start:2px solid transparent}
.toc li a:hover{color:var(--text);border-color:var(--accent);text-decoration:none}
.summary{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:26px 28px;margin-bottom:28px}
.summary h2{margin:0 0 14px;font-size:18px}
.points{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.point{background:var(--surface-2);border:1px solid var(--line);border-radius:14px;padding:16px}
.point svg{width:22px;height:22px;color:var(--ink);margin-bottom:6px}
.point b{display:block;font-weight:600;font-size:15.5px;line-height:1.5}.point span{color:var(--muted);font-size:14px;line-height:1.7}
section.s{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:26px 28px;margin-bottom:16px;scroll-margin-top:84px}
section.s h2{display:flex;align-items:center;gap:12px;margin:0 0 10px;font-size:19px;font-weight:600;line-height:1.5}
.num{flex:none;width:30px;height:30px;border-radius:9px;background:var(--accent-soft);color:var(--ink);display:grid;place-items:center;font-size:14px;font-weight:600}
section.s p{margin:0 0 10px;color:var(--text)}section.s p:last-child{margin-bottom:0}
section.s ul{margin:6px 0 0;padding-inline-start:20px}section.s li{margin:4px 0}section.s li::marker{color:var(--ink)}
.table{width:100%;border-collapse:separate;border-spacing:0;margin-top:8px;font-size:15px;border:1px solid var(--line);border-radius:12px;overflow:hidden}
.table th,.table td{padding:12px 14px;text-align:start;vertical-align:top;border-bottom:1px solid var(--line)}
.table th{background:var(--surface-2);font-weight:600;font-size:13.5px;color:var(--muted)}.table tr:last-child td{border-bottom:0}
.tag{display:inline-block;font-size:12.5px;padding:2px 10px;border-radius:999px;font-weight:500;white-space:nowrap}
.no{background:color-mix(in srgb,#16a34a 12%,transparent);color:#15803d}.dev{background:var(--accent-soft);color:var(--ink)}.ads{background:color-mix(in srgb,#d97706 14%,transparent);color:#b45309}
@media (prefers-color-scheme:dark){.no{color:#4ade80}.ads{color:#fbbf24}}
.contact{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:8px;background:var(--accent);color:#fff;padding:10px 18px;border-radius:12px;font-weight:500;font-size:15px}.btn:hover{text-decoration:none;filter:brightness(1.07)}
footer{border-top:1px solid var(--line);padding:28px 0;color:var(--muted);font-size:14px}
footer .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.apps{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;padding-bottom:72px}
.card{display:flex;align-items:center;gap:14px;background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px;box-shadow:var(--shadow);transition:transform .15s ease,border-color .15s ease}
.card:hover{transform:translateY(-2px);border-color:color-mix(in srgb,var(--accent) 40%,var(--line))}
.card .badge{width:48px;height:48px;border-radius:13px;font-size:21px;box-shadow:none}
.card .n{font-weight:600;font-size:15.5px;line-height:1.5;color:var(--text)}
.card .l{display:flex;gap:14px;font-size:13.5px}
@media (max-width:860px){.grid{grid-template-columns:1fr}.toc{display:none}.points{grid-template-columns:1fr}section.s,.summary{padding:22px 20px}.hero{padding-top:36px}}
"""

MARK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F3E2B5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 15.4 6.8 18.1l1-5.8L3.5 8.2l5.9-.9z"/></svg>'
ICON_LOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M11 18h2"/></svg>'
ICON_SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6z"/><path d="M9 12l2 2 4-4"/></svg>'
ICON_MAIL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 6.5L12 13l8.5-6.5"/></svg>'


def head(title, lang, accent, desc):
    d = "rtl" if lang == "ar" else "ltr"
    return f"""<!doctype html><html lang="{lang}" dir="{d}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="preload" href="/assets/ReadexPro-Variable.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="/assets/site.css"><style>:root{{--accent:{accent}}}</style></head><body>"""


def topbar(lang, other_href):
    if lang == "ar":
        nav = f'<a href="/">التطبيقات</a><a href="mailto:{EMAIL}">تواصل</a>'
        sw = f'<span class="lang"><a class="on" href="#">العربية</a><a href="{other_href}">English</a></span>'
    else:
        nav = f'<a href="/">Apps</a><a href="mailto:{EMAIL}">Contact</a>'
        sw = f'<span class="lang"><a href="{other_href}">العربية</a><a class="on" href="#">English</a></span>'
    return f"""<header class="topbar"><div class="wrap"><a class="brand" href="/"><span class="mark">{MARK}</span>appscitadel</a>
<nav class="nav">{nav}{sw if other_href else ''}</nav></div></header>"""


def footer(lang):
    if lang == "ar":
        return f'<footer><div class="wrap"><span>© 2026 appscitadel — OFQ Labs. جميع الحقوق محفوظة.</span><span><a href="/">كل التطبيقات</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span></div></footer></body></html>'
    return f'<footer><div class="wrap"><span>© 2026 appscitadel — OFQ Labs. All rights reserved.</span><span><a href="/">All apps</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span></div></footer></body></html>'


def stored_on_device(kind, lang):
    if lang == "ar":
        return "المفضلة وآخر فتوى قرأتها وإعدادات القراءة (حجم الخط والمظهر)" if kind == "reader" else "تقدّمك في المراحل والنقاط والإعدادات (الصوت والمظهر)"
    return "favourites, last read item and reading settings (font size, theme)" if kind == "reader" else "level progress, points and settings (sound, theme)"


def privacy_ar(pkg, name, accent, kind, glyph):
    secs = [
        ("intro", "من نحن ونطاق السياسة", f"<p>تطبيق «{name}» من تطوير <b>appscitadel</b> (حساب المطوّر OFQ Labs على Google Play). توضّح هذه السياسة ما يحدث للبيانات عند استخدامك للتطبيق، وتنطبق على التطبيق فقط وليس على مواقع أو خدمات أطراف أخرى.</p>"),
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
    return (head(f"سياسة الخصوصية — {name}", "ar", accent, f"سياسة الخصوصية لتطبيق {name} من appscitadel")
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
<section class="s" id="contact"><h2><span class="num">{len(secs)+1}</span>التواصل</h2><div class="contact"><p>لأي سؤال أو طلب بخصوص الخصوصية يسعدنا تواصلك.</p><a class="btn" href="mailto:{EMAIL}?subject={name}">{ICON_MAIL}{EMAIL}</a></div></section>
</div></div></main>""" + footer("ar"))


def privacy_en(pkg, name_ar, name, accent, kind, glyph):
    secs = [
        ("intro", "Who we are and scope", f"<p>{name} ({name_ar}) is developed by <b>appscitadel</b> (developer account OFQ Labs on Google Play). This policy explains what happens to data when you use the app. It covers this app only, not third-party sites or services.</p>"),
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
    return (head(f"Privacy Policy — {name}", "en", accent, f"Privacy policy for {name} by appscitadel")
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
<section class="s" id="contact"><h2><span class="num">{len(secs)+1}</span>Contact</h2><div class="contact"><p>Questions or requests about privacy? We're happy to help.</p><a class="btn" href="mailto:{EMAIL}?subject={name}">{ICON_MAIL}{EMAIL}</a></div></section>
</div></div></main>""" + footer("en"))


def index():
    cards = "".join(
        f'<div class="card" style="--accent:{a}"><span class="badge">{g}</span><div><div class="n">{n}</div>'
        f'<div class="l"><a href="https://play.google.com/store/apps/details?id=com.appscitadel.{p}">Google Play</a>'
        f'<a href="/privacy/{p}.html">سياسة الخصوصية</a></div></div></div>'
        for p, n, _e, a, _k, g in APPS)
    return (head("appscitadel — تطبيقات وألعاب عربية", "ar", "#0F5C4A", "تطبيقات وألعاب عربية هادفة من appscitadel على Google Play")
            + topbar("ar", "")
            + f"""<main class="wrap"><div class="hero"><h1>تطبيقات وألعاب عربية<br>مصمّمة باحترام لوقتك</h1>
<p class="lead">نطوّر تطبيقات تعليمية وألعاب ذكاء عربية خفيفة، تعمل بدون إنترنت، ولا تجمع بياناتك الشخصية.</p>
<div class="meta"><a class="btn" href="{DEV_URL}">كل تطبيقاتنا على Google Play</a></div></div>
<div class="apps">{cards}</div></main>""" + footer("ar"))


def main():
    (ROOT / "assets" / "site.css").write_text(CSS.strip(), encoding="utf-8")
    out = ROOT / "privacy"
    out.mkdir(exist_ok=True)
    for p, n, e, a, k, g in APPS:
        (out / f"{p}.html").write_text(privacy_ar(p, n, a, k, g), encoding="utf-8")
        (out / f"{p}-en.html").write_text(privacy_en(p, n, e, a, k, g), encoding="utf-8")
    (ROOT / "index.html").write_text(index(), encoding="utf-8")
    print(f"built {len(APPS)} apps x 2 languages + index")


if __name__ == "__main__":
    main()
