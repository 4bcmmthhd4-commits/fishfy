#!/usr/bin/env python3
"""Generate 'Wie funktioniert Fishfy' HTML + i18n keys from iOS Localizable.strings."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LANG_FILES = {
    "de": ROOT / "fishfy/de.lproj/Localizable.strings",
    "en": ROOT / "fishfy/en.lproj/Localizable.strings",
    "nl": ROOT / "fishfy/nl.lproj/Localizable.strings",
    "fr": ROOT / "fishfy/fr.lproj/Localizable.strings",
    "lb": ROOT / "fishfy/lb.lproj/Localizable.strings",
}


def parse_strings(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for m in re.finditer(r'^"([^"]+)"\s*=\s*"(.*)"\s*;\s*$', text, re.MULTILINE):
        k, v = m.group(1), m.group(2)
        out[k] = v.replace('\\"', '"').replace("\\n", "\n")
    return out


def keyify(fullk: str) -> str:
    return fullk.replace("prognosis_explanation.", "pe_").replace(".", "_")


CARDS = [
    ("sec", "prognosis_explanation.section_forecast", None, False),
    ("how-fish", "prognosis_explanation.target_fish", "prognosis_explanation.target_fish_body", False),
    ("how-gauge", "prognosis_explanation.score", "prognosis_explanation.score_body", False),
    ("how-wrench", "prognosis_explanation.bait_tech", "prognosis_explanation.bait_tech_body", False),
    ("how-arrows-v", "prognosis_explanation.depth_lead", "prognosis_explanation.depth_lead_body", False),
    ("sec", "prognosis_explanation.section_influence", None, False),
    ("how-sliders", "prognosis_explanation.water_conditions", "prognosis_explanation.water_conditions_body", False),
    ("how-thermometer", "prognosis_explanation.water_temp", "prognosis_explanation.water_temp_body", False),
    ("how-clock", "prognosis_explanation.time_season", "prognosis_explanation.time_season_body", False),
    ("sec", "prognosis_explanation.section_special", None, False),
    ("how-sparkles", "prognosis_explanation.forecast", "prognosis_explanation.forecast_body", False),
    ("how-mappin", "prognosis_explanation.spots", "prognosis_explanation.spots_body", False),
    ("how-wind", "prognosis_explanation.wind_map", "prognosis_explanation.wind_map_body", False),
    ("how-camera", "prognosis_explanation.catches", "prognosis_explanation.catches_body", False),
    ("how-transfer", "prognosis_explanation.transfer", "prognosis_explanation.transfer_body", False),
    ("how-share", "prognosis_explanation.spot_transfer", "prognosis_explanation.spot_transfer_body", False),
    ("how-bulb", "prognosis_explanation.similar", "prognosis_explanation.similar_body", False),
    ("how-map", "prognosis_explanation.map", "prognosis_explanation.map_body", False),
    ("how-bell", "prognosis_explanation.notifications", "prognosis_explanation.notifications_body", False),
    ("how-cloud", "prognosis_explanation.backup", "prognosis_explanation.backup_body", False),
    ("how-chart-bar", "prognosis_explanation.stats", "prognosis_explanation.stats_body", False),
    ("how-people", "prognosis_explanation.beginners_pros", "prognosis_explanation.beginners_pros_body", False),
    ("sec", "prognosis_explanation.section_free", None, False),
    ("how-gift", "prognosis_explanation.free", "prognosis_explanation.free_body", False),
    ("how-star", "prognosis_explanation.fishfy_pro", "prognosis_explanation.fishfy_pro_body", False),
    ("sec", "prognosis_explanation.section_honest", None, False),
    ("how-hand", "prognosis_explanation.no_guarantee", "prognosis_explanation.no_guarantee_body", True),
    ("how-trend", "prognosis_explanation.we_learn", "prognosis_explanation.we_learn_body", True),
]

SPRITE = """
<symbol id="how-fish" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M6 13c-1.5 0-3 1-3 2s1.5 2 3 2 4-1.5 4-4-2-4-4-4-1.5 1-3 1-3-1-3-2 1.5-2 3-2"/><path d="M16.5 8.5c2 2 2.5 5.5 0 7.5M18 6l2-2M18 18l2 2"/></symbol>
<symbol id="how-gauge" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M12 14v3M4 15a8 8 0 1 1 16 0"/><path d="M12 15l3-5"/></symbol>
<symbol id="how-wrench" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 1 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></symbol>
<symbol id="how-arrows-v" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M8 11V5M5 8l3-3 3 3M16 13v6M19 16l-3 3-3-3"/></symbol>
<symbol id="how-sliders" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M9 8h6M15 16h6M7 4h2"/></symbol>
<symbol id="how-thermometer" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 1 1 4 0z"/></symbol>
<symbol id="how-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></symbol>
<symbol id="how-sparkles" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M9.5 2l1 4 4 1-4 1-1 4-1-4-4-1 4-1 1-4zM16 11l.5 2 2 .5-2 .5-.5 2-.5-2-2-.5 2-.5.5-2z"/></symbol>
<symbol id="how-mappin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-4.5 7-11a7 7 0 1 0-14 0c0 6.5 7 11 7 11z"/><ellipse cx="12" cy="10" rx="3" ry="1.5"/></symbol>
<symbol id="how-wind" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M3 8h7a3 3 0 1 0-3-3M5 12h11a4 4 0 1 1-4 4M3 16h15"/></symbol>
<symbol id="how-camera" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9h3l2-2h6l2 2h3a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2z"/><circle cx="12" cy="14" r="3"/></symbol>
<symbol id="how-transfer" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8 12h8M15 9l3 3-3 3M9 15l-3-3 3-3"/></symbol>
<symbol id="how-share" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v8M9 10l3-3 3 3"/></symbol>
<symbol id="how-bulb" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 22h4M12 2a6 6 0 0 0-3 11v2h6v-2a6 6 0 0 0-3-11z"/></symbol>
<symbol id="how-map" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14"/></symbol>
<symbol id="how-bell" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 1 1 12 0c0 7 3 7 3 7H3s3 0 3-7M10 21h4"/></symbol>
<symbol id="how-cloud" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></symbol>
<symbol id="how-chart-bar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M4 19V5M8 19v-6M12 19V9M16 19v-3M20 19v-8"/></symbol>
<symbol id="how-people" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></symbol>
<symbol id="how-gift" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="13" rx="2"/><path d="M12 8V21M3 12h18M12 8H9.5a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 2.5-5a2.5 2.5 0 0 1 0 5H12z"/></symbol>
<symbol id="how-star" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.4 7.4h7.6l-6 4.6 2.3 7-6.3-4.6-6.3 4.6 2.3-7-6-4.6h7.6z"/></symbol>
<symbol id="how-hand" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M12 11V3M8 11V6M16 11V7M4 11v2a8 8 0 0 0 16 0v-6a2 2 0 0 0-2-2h-1"/></symbol>
<symbol id="how-trend" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 12l4-4 4 4 6-6M17 8h4v4"/></symbol>
"""


def main() -> None:
    D = {lang: parse_strings(p) for lang, p in LANG_FILES.items()}

    def tr(lang: str, key: str) -> str:
        return D[lang].get(key) or D["en"].get(key) or key

    i18n: dict[str, dict[str, str]] = {lang: {} for lang in LANG_FILES}

    for lang in LANG_FILES:
        i18n[lang]["features_title"] = tr(lang, "prognosis_explanation.title")
        i18n[lang]["features_subtitle"] = tr(lang, "prognosis_explanation.intro")
        i18n[lang]["nav_features"] = tr(lang, "more.how_it_works")
        i18n[lang]["pe_tech_title"] = tr(lang, "prognosis_explanation.tech_title")
        i18n[lang]["pe_tech_body"] = tr(lang, "prognosis_explanation.tech_body")

    lines: list[str] = []
    lines.append('            <div class="section-header">')
    lines.append('                <h2 data-i18n="features_title"></h2>')
    lines.append('                <p data-i18n="features_subtitle"></p>')
    lines.append("            </div>")
    lines.append('            <svg class="how-sprite" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">')
    for ln in SPRITE.strip().split("\n"):
        lines.append("                " + ln)
    lines.append("            </svg>")
    lines.append('            <div class="how-it-inner">')

    tones = ["blue", "orange", "green", "purple"]
    tone_i = 0

    for icon, tk, bk, orange in CARDS:
        if icon == "sec":
            kk = keyify(tk)
            for lang in LANG_FILES:
                i18n[lang][kk] = tr(lang, tk)
            lines.append(f'                <h3 class="how-section-heading" data-i18n="{kk}"></h3>')
            continue
        kt, kb = keyify(tk), keyify(bk)
        for lang in LANG_FILES:
            i18n[lang][kt] = tr(lang, tk)
            i18n[lang][kb] = tr(lang, bk)
        if orange:
            card_cls = "how-card feature-card orange-accent"
            tone = "orange"
        else:
            card_cls = "how-card feature-card"
            tone = tones[tone_i % 4]
            tone_i += 1
        fill_cls = " is-filled" if icon == "how-star" else ""
        lines.append(f'                <div class="{card_cls}">')
        lines.append(
            f'                    <div class="how-card-icon feature-icon {tone}{fill_cls}" aria-hidden="true">\n'
            f'                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="26" height="26">'
            f'<use href="#{icon}"/></svg>\n'
            f"                    </div>"
        )
        lines.append(f'                    <h4 data-i18n="{kt}"></h4>')
        lines.append(f'                    <p data-i18n="{kb}"></p>')
        lines.append("                </div>")

    lines.append('                <div class="how-tech">')
    lines.append('                    <h3 data-i18n="pe_tech_title"></h3>')
    lines.append('                    <p data-i18n="pe_tech_body"></p>')
    lines.append("                </div>")
    lines.append("            </div>")

    out_dir = Path(__file__).resolve().parent
    (out_dir / "_how_inner.html").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out_dir / "_how_i18n.json").write_text(json.dumps(i18n, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote _how_inner.html and _how_i18n.json")


if __name__ == "__main__":
    main()
