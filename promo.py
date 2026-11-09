"""Writes /promo.json: the cross-promo feed the apps' home «جرّب ألعابنا» card rotates through.

Called by build.py. Schema v1 (apps read only these keys and ignore anything new):
  v, updated, rotateSeconds, games[] = {id, platform, name{<21 locales>}, icon, url, family, weight, countries, active}
name carries every key in LOCALES (always ar and en); clients pick the app locale, then en, then ar.
Names live in promo_names.json (keyed by apps.json id); a listed game missing a locale fails the build.
Only apps.json entries with live:true and a Play URL are listed, and only when their icon file exists in the site.
Edit apps.json (or the maps below), run `python -X utf8 build.py`, commit, push: every app picks it up within 6 h.
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://apps.ofqventures.com"
OUT = ROOT / "promo.json"
NAMES = ROOT / "promo_names.json"
ROTATE_SECONDS = 15
# Same 21 locales as the games' Play listings. Chinese uses region keys; everything else is 2-letter.
LOCALES = ("en", "ar", "de", "es", "fa", "fr", "hi", "id", "it", "ja", "ko", "ms", "nl", "pl", "pt", "ru",
           "th", "tr", "vi", "zh-CN", "zh-TW")

# Family = the `appFamily` constant in each app's lib/config.dart; an app shows its own family first.
FAMILY_BY_ID = {
    "timoz": "party",
    "abaqeragame": "trivia",
    "ehzerla3eb": "football",
    "ehzerla3eb2": "football",
    "mathpuzzle": "math",
    "fatawyibnbaz": "religious",
}
FAMILY_BY_CATEGORY = {"كلمات": "word", "صور": "word", "ألغاز": "word", "ذكاء": "word",
                      "كرة قدم": "football", "ديني": "religious", "ألعاب جماعية": "party"}

# 3 = top earners, 2 = new flagship games, 1 = everything else.
WEIGHT = {"fatawyibnbaz": 3, "sabakalemat": 3, "wasla1": 3,
          "timoz": 2, "raflo": 2, "fakkaha": 2, "lammah": 2}


def short(name):
    """Store title without its subtitle: «سبع كلمات - لعبة ألغاز وكلمات» -> «سبع كلمات»."""
    return re.split(r"\s+-\s+|\s*:\s*", name, maxsplit=1)[0].strip()


def names_for(a, table):
    """All 21 locale names for one app; ar/en default to the apps.json titles."""
    row = {"ar": short(a["nameAr"]), "en": short(a["nameEn"]), **table.get(a["id"], {})}
    missing = [k for k in LOCALES if not str(row.get(k) or "").strip()]
    assert not missing, f"promo_names.json: {a['id']} has no name for {', '.join(missing)}"
    return {k: row[k].strip() for k in LOCALES}


def games(apps):
    table = json.loads(NAMES.read_text(encoding="utf8")) if NAMES.exists() else {}
    out, skipped = [], []
    for a in sorted(apps, key=lambda a: a.get("order", 999)):
        if not a.get("live") or not a.get("play"):
            continue
        icon = a.get("iconPng") or ""
        if not icon or not (ROOT / icon).is_file():
            skipped.append(a["id"])
            continue
        out.append({
            "id": a["package"],
            "platform": "android",
            "name": names_for(a, table),
            "icon": f"{SITE}/{icon}",
            "url": a["play"],
            "family": FAMILY_BY_ID.get(a["id"], FAMILY_BY_CATEGORY.get(a.get("category"), "word")),
            "weight": WEIGHT.get(a["id"], 1),
            "countries": None,
            "active": True,
        })
    return out, skipped


def write(apps):
    items, skipped = games(apps)
    updated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if OUT.exists():  # keep the timestamp stable when nothing changed, so rebuilds make no diff
        try:
            old = json.loads(OUT.read_text(encoding="utf8"))
            if old.get("games") == items and old.get("rotateSeconds") == ROTATE_SECONDS:
                updated = old.get("updated", updated)
        except ValueError:
            pass
    feed = {"v": 1, "updated": updated, "rotateSeconds": ROTATE_SECONDS, "games": items}
    text = json.dumps(feed, ensure_ascii=False, indent=1) + "\n"
    assert len(text.encode("utf8")) < 40_000, "promo.json must stay under 40 KB"
    OUT.write_text(text, encoding="utf8")
    if skipped:
        print("promo.json: no icon file, skipped:", ", ".join(skipped))
    print(f"promo.json: {len(items)} games")
    return feed


if __name__ == "__main__":
    write(json.loads((ROOT / "apps.json").read_text(encoding="utf8")))
