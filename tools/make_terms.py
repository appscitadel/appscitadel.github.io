# Terms of use for the standalone game folders (same layout as harrif/terms.html), Arabic + English on one page.
# Run: python -X utf8 tools/make_terms.py   (re-runnable; also links each privacy.html to its terms.html)
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPDATED = "2026-11-06"
EULA = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"

# folder: (Arabic name, English name, theme colour, online play?)
GAMES = {
    "fakkaha": ("فكّها!", "Fakkaha", "#4E7A2E", True),
    "raflo": ("رافلو", "Raflo", "#8A4A22", False),
    "bisbis": ("بسبس", "Bisbis", "#7a3f22", False),
    "reefy": ("ريفي سوليتير", "REEFY Solitaire", "#0b3d5c", False),
    "marblo": ("ماربلو", "MARBLO", "#14102e", False),
    "harb-elboya": ("حرب البوية", "Harb El Boya", "#7a3f22", False),
    "lammah": ("لمّاح", "Lammah", "#2563eb", False),
    "triplo": ("تريبلو", "TRIPLO", "#2b1b5e", False),
    "nudgo": ("ندجو", "NUDGO", "#0f2e31", False),
    "fogwick": ("فوجويك", "FOGWICK", "#2b3a4a", False),
    "tanglo": ("تانجلو", "TANGLO", "#8f5322", False),
    "buzzle": ("بازل", "BUZZLE", "#d99a1e", False),
    "flingo": ("فلينجو", "FLINGO", "#e8641e", False),
}


def page(ar, en, colour, online):
    ar_online = """  <h2>اللعب أونلاين واسم اللعب</h2>
  <ul>
    <li>اسم اللعب اللي بتكتبه بيظهر للاعب اللي بتنافسه.</li>
    <li><b>ممنوع</b> أي اسم أو محتوى مسيء: شتيمة، كراهية أو تمييز، تحرّش أو تهديد، محتوى جنسي، انتحال شخصية، أو بيانات شخصية لحد تاني. ممكن نغيّر أي اسم مخالف ونوقف الحساب اللي استخدمه.</li>
    <li>ممنوع الغش أو استغلال الأخطاء أو التلاعب في النتايج، والنتايج المشبوهة بتتشال.</li>
  </ul>
""" if online else ""
    en_online = """    <p><b>Online play and display names.</b> The display name you choose is shown to your opponent. No offensive names or content: profanity, hate or discrimination, harassment or threats, sexual content, impersonation, or other people's personal data. We may change an offending name and suspend the account that used it. No cheating, exploiting bugs or manipulating results; suspicious results are removed.</p>
""" if online else ""
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>شروط الاستخدام • {ar}</title>
<meta name="theme-color" content="{colour}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Lalezar&display=swap" rel="stylesheet">
<style>
  .doc {{ text-align: right; max-width: 720px; }}
  .doc h1 {{ font-family: Lalezar, Cairo, sans-serif; font-weight: 400; }}
  .doc h2 {{ font-size: 1.1rem; margin-top: 1.6rem; }}
  .doc p, .doc li {{ line-height: 1.9; }}
  .doc .en {{ direction: ltr; text-align: left; border-top: 1px solid rgba(0,0,0,.12); margin-top: 2rem; padding-top: 1rem; }}
</style>
</head>
<body style="font-family:Cairo,sans-serif;margin:0;padding:1rem;background:#f6f3ee;color:#222">
<main class="doc" style="margin:0 auto">
  <h1>شروط الاستخدام</h1>
  <p>الناشر: OFQ Labs (OFQ Ventures). آخر تحديث: {UPDATED}</p>
  <p>باستخدامك لعبة «{ar}» إنت موافق على الشروط دي وعلى <a href="privacy.html">سياسة الخصوصية</a>.</p>
  <h2>استخدام اللعبة</h2>
  <p>اللعبة مجانية لاستخدامك الشخصي. ممنوع تنسخها أو تبيعها أو تعدّلها أو تفك شفرتها أو تعيد نشر محتواها، أو تستخدمها بطريقة تضر اللعبة أو غيرك.</p>
{ar_online}  <h2>العملات والإعلانات</h2>
  <p>العملات والتلميحات والنجوم جوه اللعبة ملهاش قيمة مالية ومينفعش تتباع أو تتحوّل لفلوس أو تتنقل لحد تاني. مفيش شراء من جوه اللعبة. إعلانات المكافأة اختيارية دايمًا، والإعلانات من Google AdMob وشركائها، ومش مسؤولين عن المواقع أو المنتجات اللي بتعلن عنها.</p>
  <h2>الملكية الفكرية</h2>
  <p>اللعبة وتصميمها وشعارها ملك OFQ Ventures.</p>
  <h2>إخلاء المسؤولية</h2>
  <p>اللعبة متاحة «زي ما هي». ممكن نغيّر أو نوقف أي جزء منها، وممكن نعدّل الشروط دي ونغيّر تاريخ آخر تحديث فوق. ومفيش حاجة هنا بتقلّل من حقوقك في قانون حماية المستهلك في بلدك. على آيفون، الشروط دي بتكمّل <a href="{EULA}">اتفاقية Apple القياسية للمستخدم (EULA)</a>.</p>
  <h2>القانون</h2>
  <p>الشروط دي خاضعة لقوانين جمهورية مصر العربية، من غير ما تمس القواعد الإلزامية لحماية المستهلك في بلدك.</p>
  <h2>تواصل معانا</h2>
  <p><a href="mailto:contact@ofqventures.com">contact@ofqventures.com</a></p>

  <section class="en">
    <h2>Terms of use (English)</h2>
    <p>Publisher: OFQ Labs (OFQ Ventures). App: {en}. Last updated: {UPDATED}. By using {en} you agree to these terms and the <a href="privacy.html">privacy policy</a>.</p>
    <p><b>Use of the game.</b> The game is free for your personal use. You may not copy, sell, modify, decompile or republish it or its content, or use it in a way that harms the game or others.</p>
{en_online}    <p><b>Coins and ads.</b> In-game coins, hints and stars have no monetary value and cannot be sold, exchanged for money or transferred. There are no in-app purchases. Rewarded ads are always optional. Ads come from Google AdMob and its partners; we are not responsible for the sites or products they promote.</p>
    <p><b>Intellectual property.</b> The game, its design and its logo belong to OFQ Ventures.</p>
    <p><b>Disclaimer.</b> The game is provided "as is" and may change or be discontinued. We may update these terms and the last-updated date above. Nothing here limits your rights under your local consumer protection law. On iOS these terms supplement <a href="{EULA}">Apple's Standard EULA</a>.</p>
    <p><b>Governing law.</b> These terms are governed by the laws of the Arab Republic of Egypt, without prejudice to the mandatory consumer protection rules of your country.</p>
    <p>Contact: <a href="mailto:contact@ofqventures.com">contact@ofqventures.com</a></p>
  </section>
</main>
</body>
</html>
"""


for folder, (ar, en, colour, online) in GAMES.items():
    (ROOT / folder / "terms.html").write_text(page(ar, en, colour, online), encoding="utf-8")
    pp = ROOT / folder / "privacy.html"
    html = pp.read_text(encoding="utf-8")
    if 'href="terms.html"' not in html:
        assert html.count('<section class="en"') == 1, folder
        html = html.replace('<section class="en"', '<p><a href="terms.html">شروط الاستخدام</a></p>\n\n  <section class="en"', 1)
        i = html.rindex("</section>")
        html = html[:i] + '  <p><a href="terms.html">Terms of use</a></p>\n  ' + html[i:]
        pp.write_text(html, encoding="utf-8")
    print(folder, "ok")
