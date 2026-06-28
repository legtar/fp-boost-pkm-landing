# -*- coding: utf-8 -*-
"""Static site generator for the ФП-БУСТ-ПКМ-01 landing.

Generates SEO-optimized inner pages (product types + calculator) that share the
homepage's header/footer/styles, each with breadcrumbs, Open Graph and JSON-LD
(BreadcrumbList + Product/Service + FAQPage). Also regenerates sitemap.xml.

Run:  python tools/build_site.py
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://legtar.github.io/fp-boost-pkm-landing"
ORG_ID = f"{BASE}/#org"

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='7' fill='%230f1838'/%3E%3Cg fill='%23f0b36f'%3E"
           "%3Crect x='7' y='13' width='3' height='6' rx='1.5'/%3E%3Crect x='12' y='9' width='3' height='14' rx='1.5'/%3E"
           "%3Crect x='17' y='6' width='3' height='20' rx='1.5'/%3E%3Crect x='22' y='11' width='3' height='10' rx='1.5'/%3E"
           "%3C/g%3E%3C/svg%3E")


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def head(page) -> str:
    p = "../"  # all generated pages live one level deep
    url = f"{BASE}/{page['slug']}/"
    schema = json.dumps(page["schema"], ensure_ascii=False, indent=2)
    extra_css = page.get("extra_head", "")
    return f"""<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{esc(page['title'])}</title>
    <meta name="description" content="{esc(page['description'])}">
    <meta name="theme-color" content="#0f1838">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="ru_RU">
    <meta property="og:site_name" content="Техносерт Груп — Fire Protection Boost">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{esc(page['title'])}">
    <meta property="og:description" content="{esc(page['description'])}">
    <meta property="og:image" content="{BASE}/assets/img/og-cover.jpg">
    <link rel="icon" href="{FAVICON}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
    <link rel="stylesheet" href="{p}styles.css">
    {extra_css}
    <script src="{p}script.js" defer></script>
    <script type="application/ld+json">
{schema}
    </script>
  </head>
  <body>
    <a class="skip-nav" href="#main">К содержанию</a>
    <header class="site-header is-solid" data-header>
      <a class="brand" href="{p}">
        <span class="brand-mark" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span></span>
        <span class="brand-copy"><span>Fire Protection Boost</span><strong>Техносерт Груп</strong></span>
      </a>
      <nav class="site-nav" aria-label="Основная навигация">
        <a href="{p}kabelnye-prohodki/">Кабельные</a>
        <a href="{p}shinoprovody/">Шинопроводы</a>
        <a href="{p}truby-vozduhovody/">Трубы и воздуховоды</a>
        <a href="{p}kalkulyator/">Калькулятор</a>
        <a href="{p}#certificates">Сертификаты</a>
      </nav>
      <div class="header-actions">
        <a class="header-phone" href="tel:+74950000000">
          <span class="header-phone-label">Отдел продаж</span>
          <span class="header-phone-number">+7 (495) 000-00-00</span>
        </a>
        <a class="button button-primary header-cta" href="{p}#contacts">Получить расчёт КП</a>
      </div>
    </header>
    <main id="main">"""


def breadcrumbs(page) -> str:
    p = "../"
    return f"""
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <div class="container">
          <a href="{p}">Главная</a>
          <span aria-hidden="true">/</span>
          <span>{esc(page['crumb'])}</span>
        </div>
      </nav>"""


def footer() -> str:
    p = "../"
    return f"""
    </main>
    <footer class="site-footer">
      <div class="container footer-grid">
        <div>
          <strong>ООО «Техносерт Груп»</strong>
          <p>г. Москва, Старокалужское шоссе, д.62, пом. 11, ОГРН 1177746413790</p>
          <nav class="footer-nav" aria-label="Разделы">
            <a href="{p}kabelnye-prohodki/">Кабельные проходки</a>
            <a href="{p}shinoprovody/">Проходы шинопроводов</a>
            <a href="{p}truby-vozduhovody/">Трубы и воздуховоды</a>
            <a href="{p}kombinirovannye-prohodki/">Комбинированные проходки</a>
            <a href="{p}kalkulyator/">Калькулятор подбора узла</a>
          </nav>
        </div>
        <div class="footer-links">
          <a href="tel:+74950000000">+7 (495) 000-00-00</a>
          <a href="mailto:info@fireprotectionboost.ru">info@fireprotectionboost.ru</a>
          <a href="https://www.fireprotectionboost.ru">www.fireprotectionboost.ru</a>
        </div>
      </div>
    </footer>
    <a class="mobile-cta" href="../#contacts">Получить расчёт КП</a>
  </body>
</html>
"""


def breadcrumb_schema(page):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": f"{BASE}/{page['slug']}/"},
        ],
    }


def faq_schema(faq):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }


def product_schema(page):
    return {
        "@type": "Product",
        "name": page["product_name"],
        "category": "Огнезащита / огнестойкие проходки",
        "brand": {"@type": "Brand", "name": "ФП-БУСТ"},
        "manufacturer": {"@id": ORG_ID},
        "description": page["description"],
        "image": f"{BASE}/assets/img/og-cover.jpg",
    }


def render_product(page) -> None:
    faq_html = "".join(
        f"""
          <details class="faq-item">
            <summary>{esc(q)}</summary>
            <p>{esc(a)}</p>
          </details>"""
        for q, a in page["faq"]
    )
    feature_html = "".join(f"<li>{esc(x)}</li>" for x in page["features"])
    app_html = "".join(f"<li>{esc(x)}</li>" for x in page["applications"])
    eit_html = "".join(f"<span>{v}</span>" for v in ["45", "60", "90", "120", "150", "180"])
    intro_html = "".join(f"<p>{esc(par)}</p>" for par in page["intro"])
    related = [r for r in PRODUCT_PAGES if r["slug"] != page["slug"]]
    related_html = "".join(
        f'<a class="related-card" href="../{r["slug"]}/"><strong>{esc(r["crumb"])}</strong><span>{esc(r["short"])}</span></a>'
        for r in related
    )

    page["schema"] = {"@context": "https://schema.org", "@graph": [
        breadcrumb_schema(page), product_schema(page), faq_schema(page["faq"]),
    ]}

    body = f"""
      <section class="section section-light page-hero">
        <div class="container">
          <p class="eyebrow">{esc(page['eyebrow'])}</p>
          <h1>{esc(page['h1'])}</h1>
          <div class="page-lead">{intro_html}</div>
          <div class="hero-actions">
            <a class="button button-primary" href="../kalkulyator/">Подобрать узел в калькуляторе</a>
            <a class="button button-secondary" href="../#contacts">Получить расчёт КП</a>
          </div>
        </div>
      </section>

      <section class="section section-tinted">
        <div class="container split-cols">
          <div class="prose">
            <h2>Применение</h2>
            <ul class="ticks">{app_html}</ul>
            <h2>Характеристики и преимущества</h2>
            <ul class="ticks">{feature_html}</ul>
          </div>
          <aside class="spec-aside">
            <h3>Пределы огнестойкости {esc(page['eit_letter'])}, минут</h3>
            <div class="eit-track">{eit_html}</div>
            <dl class="spec-list">
              <div><dt>Сертификация</dt><dd>{esc(page['cert'])}</dd></div>
              <div><dt>Маркировка</dt><dd>{esc(page['marking'])}</dd></div>
              <div><dt>Материалы заделки</dt><dd>пена ФП-БУСТ-01, герметик ФП-БУСТ-05, минплита ≥150 кг/м³</dd></div>
            </dl>
            <a class="button button-primary full" href="../#contacts">Запросить КП и спецификацию</a>
          </aside>
        </div>
      </section>

      <section class="section section-light">
        <div class="container">
          <h2>Частые вопросы</h2>
          <div class="faq-list">{faq_html}</div>
        </div>
      </section>

      <section class="section section-tinted">
        <div class="container">
          <h2>Другие типы проходок ФП-БУСТ-ПКМ-01</h2>
          <div class="related-grid">{related_html}</div>
        </div>
      </section>
"""
    out = ROOT / page["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head(page) + breadcrumbs(page) + body + footer(), encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


# --------------------------- Product page content ---------------------------

PRODUCT_PAGES = [
    {
        "slug": "kabelnye-prohodki",
        "crumb": "Кабельные проходки",
        "short": "Кабели, лотки, гильзы, модульные проходки",
        "eyebrow": "Кабельные проходки",
        "h1": "Огнестойкие кабельные проходки ФП-БУСТ-ПКМ-01",
        "title": "Огнестойкие кабельные проходки ФП-БУСТ-ПКМ-01 — EIT до 180, сертификат ЕАЭС",
        "description": "Универсальные огнестойкие кабельные проходки ФП-БУСТ-ПКМ-01: гильзы, лотки, модульные проходки. Огнестойкость EIT 45–180 минут, сертификат ТР ЕАЭС 043/2017, шеф-монтаж.",
        "product_name": "Огнестойкая кабельная проходка ФП-БУСТ-ПКМ-01",
        "eit_letter": "EIT",
        "cert": "Сертификат ТР ЕАЭС 043/2017",
        "marking": "ФП-БУСТ-ПКМ-01-АхВ-4/ПМ(1)-150",
        "intro": [
            "Огнестойкие кабельные проходки ФП-БУСТ-ПКМ-01 восстанавливают предел огнестойкости стен и перекрытий в местах прохода силовых и слаботочных кабелей. Узел заделки не даёт огню и дыму распространяться между помещениями и этажами через кабельные проёмы.",
            "Система рассчитана на групповую прокладку кабелей и работает с закладными гильзами, гильзопакетами, модульными проходками, кабельными лотками и электротехническими коробами.",
        ],
        "applications": [
            "Кабель внутри закладных гильз и гильзопакетов",
            "Модульные кабельные проходки",
            "Кабельные лотки и электротехнические короба",
            "Групповая прокладка силовых и слаботочных кабелей",
        ],
        "features": [
            "Огнестойкость EIT 45, 60, 90, 120, 150 и 180 минут",
            "Сертификат соответствия ТР ЕАЭС 043/2017",
            "Надёжная работа при плотной групповой прокладке кабелей",
            "Ремонтопригодность: возможна доустановка кабелей в эксплуатируемую проходку",
        ],
        "faq": [
            ("Какой предел огнестойкости даёт кабельная проходка ФП-БУСТ-ПКМ-01?", "EIT 45, 60, 90, 120, 150 или 180 минут — в зависимости от конструкции узла, типа стены/перекрытия и заполнения проёма."),
            ("Можно ли доукладывать кабели после монтажа проходки?", "Да. Для эксплуатируемых проходок применяются разборные решения на пеноблоках ФП-БУСТ-01, позволяющие добавлять кабели без полной переделки узла."),
            ("Какие документы передаются для пожарной экспертизы?", "Сертификат ТР ЕАЭС 043/2017, протоколы испытаний и альбом типовых узлов с маркировкой и пределами огнестойкости."),
        ],
    },
    {
        "slug": "shinoprovody",
        "crumb": "Проходы шинопроводов",
        "short": "Магистральные и распределительные шинопроводы до 6300 А",
        "eyebrow": "Проходы шинопроводов",
        "h1": "Огнестойкие проходы шинопроводов ФП-БУСТ-ПКМ-01",
        "title": "Огнестойкие проходы шинопроводов ФП-БУСТ-ПКМ-01 — до 6300 А, EIT до 180",
        "description": "Огнестойкие проходы шинопроводов ФП-БУСТ-ПКМ-01 для магистральных и распределительных шинопроводов до 1000 В и 6300 А. Огнестойкость EIT 45–180, сертификат ТР ЕАЭС 043/2017.",
        "product_name": "Огнестойкий проход шинопровода ФП-БУСТ-ПКМ-01",
        "eit_letter": "EIT",
        "cert": "Сертификат ТР ЕАЭС 043/2017",
        "marking": "ФП-БУСТ-ПКМ-01-АхВ-Ш/ПМ(1)-150",
        "intro": [
            "Огнестойкие проходы шинопроводов ФП-БУСТ-ПКМ-01 герметизируют проёмы в местах прохода магистральных и распределительных шинопроводов через противопожарные преграды.",
            "Решение рассчитано на шинопроводы напряжением до 1000 В с номинальным током от 100 до 6300 А и совместимо со всеми распространёнными марками шинопроводов.",
        ],
        "applications": [
            "Магистральные шинопроводы",
            "Распределительные шинопроводы",
            "Шинопроводы напряжением до 1000 В",
            "Номинальный ток от 100 до 6300 А",
        ],
        "features": [
            "Огнестойкость EIT 45, 60, 90, 120, 150 и 180 минут",
            "Сертификат соответствия ТР ЕАЭС 043/2017",
            "Совместимость со всеми распространёнными марками шинопроводов",
            "Учитывает тепловое расширение шинопровода в узле заделки",
        ],
        "faq": [
            ("На какой ток рассчитаны проходы шинопроводов?", "На шинопроводы напряжением до 1000 В с номинальным током от 100 до 6300 А."),
            ("Подходит ли система к шинопроводам разных производителей?", "Да, узел совместим со всеми распространёнными марками магистральных и распределительных шинопроводов."),
            ("Учитывается ли нагрев и расширение шинопровода?", "Да, конструкция узла заделки рассчитана на тепловое расширение и сохраняет огнестойкость в рабочем режиме."),
        ],
    },
    {
        "slug": "truby-vozduhovody",
        "crumb": "Трубы и воздуховоды",
        "short": "Металлические трубопроводы, воздуховоды, газоходы",
        "eyebrow": "Трубопроводы и воздуховоды",
        "h1": "Огнестойкие проходы трубопроводов и воздуховодов ФП-БУСТ-ПКМ-01",
        "title": "Огнестойкие проходы труб и воздуховодов ФП-БУСТ-ПКМ-01 — EI до 180",
        "description": "Огнестойкие проходы трубопроводов, воздуховодов и газоходов ФП-БУСТ-ПКМ-01. Огнестойкость EI 45–180, добровольная сертификация ГОСТ 30247.0-94, 30247.1-94.",
        "product_name": "Огнестойкий проход трубопровода/воздуховода ФП-БУСТ-ПКМ-01",
        "eit_letter": "EI",
        "cert": "Добровольная сертификация ГОСТ 30247.0-94, 30247.1-94",
        "marking": "ФП-БУСТ-ПКМ-01-АхВ-Т/ПМ(1)-150",
        "intro": [
            "Огнестойкие проходы ФП-БУСТ-ПКМ-01 для трубопроводов и воздуховодов восстанавливают огнестойкость преграды в местах прохода инженерных сетей через стены и перекрытия.",
            "Решение применяется для металлических трубопроводов, закладных гильз, воздуховодов, газоходов и тепловой изоляции.",
        ],
        "applications": [
            "Металлические трубопроводы и закладные гильзы",
            "Воздуховоды и газоходы",
            "Тепловая изоляция трубопроводов",
            "Инженерные сети зданий и сооружений",
        ],
        "features": [
            "Огнестойкость EI 45, 60, 90, 120, 150 и 180 минут",
            "Добровольная сертификация ГОСТ 30247.0-94, 30247.1-94",
            "Совместимость с инженерными сетями и тепловой изоляцией",
            "Подходит для разных материалов стен и перекрытий",
        ],
        "faq": [
            ("Чем отличается обозначение EI от EIT?", "EI — потеря целостности (E) и теплоизолирующей способности (I); индекс T дополнительно нормирует температуру. Для труб и воздуховодов применяется предел EI 45–180 минут."),
            ("Подходит ли решение для воздуховодов с изоляцией?", "Да, узел рассчитан на воздуховоды, газоходы и трубопроводы с тепловой изоляцией."),
            ("По каким нормам сертифицировано решение?", "Добровольная сертификация по ГОСТ 30247.0-94 и ГОСТ 30247.1-94."),
        ],
    },
    {
        "slug": "kombinirovannye-prohodki",
        "crumb": "Комбинированные проходки",
        "short": "Разнотипные коммуникации через один проём",
        "eyebrow": "Комбинированные проходки",
        "h1": "Комбинированные огнестойкие проходки ФП-БУСТ-ПКМ-01",
        "title": "Комбинированные огнестойкие проходки ФП-БУСТ-ПКМ-01 — EI до 180",
        "description": "Комбинированные огнестойкие проходки ФП-БУСТ-ПКМ-01 для разнотипных коммуникаций через один проём: кабели, шинопроводы, трубы и воздуховоды. Огнестойкость EI 45–180.",
        "product_name": "Комбинированная огнестойкая проходка ФП-БУСТ-ПКМ-01",
        "eit_letter": "EI",
        "cert": "Добровольная сертификация ГОСТ 30247.0-94, 30247.1-94",
        "marking": "ФП-БУСТ-ПКМ-01-АхВ-К/ПМ(1)-150",
        "intro": [
            "Комбинированные огнестойкие проходки ФП-БУСТ-ПКМ-01 позволяют провести через один проём разнотипные коммуникации в любой комбинации: кабели, шинопроводы, трубопроводы и воздуховоды.",
            "Это упрощает проектирование и монтаж на объектах с плотными инженерными узлами и снижает число отдельных проёмов в противопожарных преградах.",
        ],
        "applications": [
            "Смешанные проёмы с кабелями и шинопроводами",
            "Совмещённые проходы труб и воздуховодов",
            "Плотные инженерные узлы и шахты",
            "Объекты с дефицитом места в противопожарных преградах",
        ],
        "features": [
            "Огнестойкость EI 45, 60, 90, 120, 150 и 180 минут",
            "Добровольная сертификация ГОСТ 30247.0-94, 30247.1-94",
            "Любая комбинация коммуникаций в одном проёме",
            "Совместимость с материалами стен и перекрытий",
        ],
        "faq": [
            ("Можно ли провести кабели и трубы через один проём?", "Да, комбинированный узел рассчитан на любую комбинацию кабелей, шинопроводов, трубопроводов и воздуховодов в одном проёме."),
            ("Снижается ли огнестойкость при смешанном проёме?", "Нет, при правильном подборе узла сохраняется требуемый предел EI 45–180 минут для всей комбинации коммуникаций."),
            ("Как подобрать комбинированный узел?", "Используйте калькулятор подбора узла или запросите расчёт КП — инженер подберёт решение под состав коммуникаций и размеры проёма."),
        ],
    },
]


def render_calculator() -> None:
    page = {
        "slug": "kalkulyator",
        "crumb": "Калькулятор подбора узла",
        "title": "Калькулятор подбора узла огнестойкой проходки ФП-БУСТ-ПКМ-01",
        "description": "Онлайн-калькулятор подбора узла огнестойкой проходки ФП-БУСТ-ПКМ-01: по типу коммуникации, размеру проёма и требуемой огнестойкости EIT/EI — маркировка узла и спецификация материалов.",
        "extra_head": '<script src="../calc.js" defer></script>',
    }
    page["schema"] = {"@context": "https://schema.org", "@graph": [
        breadcrumb_schema(page),
        {"@type": "WebApplication", "name": "Калькулятор подбора узла ФП-БУСТ-ПКМ-01",
         "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "RUB"},
         "description": page["description"], "url": f"{BASE}/{page['slug']}/"},
    ]}
    body = """
      <section class="section section-light page-hero">
        <div class="container">
          <p class="eyebrow">Калькулятор</p>
          <h1>Калькулятор подбора узла ФП-БУСТ-ПКМ-01</h1>
          <div class="page-lead">
            <p>Укажите тип коммуникации, размеры проёма и требуемый предел огнестойкости —
            калькулятор предложит предварительную маркировку узла и состав материалов заделки.
            Точный узел и спецификацию подтверждает инженер при подготовке КП.</p>
          </div>
        </div>
      </section>

      <section class="section section-tinted">
        <div class="container calc-wrap">
          <form class="calc-form" id="calcForm" novalidate>
            <div class="field">
              <label for="calcType">Тип коммуникации</label>
              <select id="calcType" name="type">
                <option value="kabel">Кабели / кабельные лотки</option>
                <option value="shina">Шинопровод</option>
                <option value="truba">Трубопровод / воздуховод</option>
                <option value="kombi">Комбинированный проём</option>
              </select>
            </div>
            <div class="field-row">
              <div class="field">
                <label for="calcW">Ширина проёма A, мм</label>
                <input type="number" id="calcW" name="w" min="50" max="3000" step="10" placeholder="например, 400">
              </div>
              <div class="field">
                <label for="calcH">Высота проёма B, мм</label>
                <input type="number" id="calcH" name="h" min="50" max="3000" step="10" placeholder="например, 200">
              </div>
            </div>
            <div class="field">
              <label for="calcEit">Требуемая огнестойкость, минут</label>
              <select id="calcEit" name="eit">
                <option>45</option><option>60</option><option>90</option>
                <option selected>120</option><option>150</option><option>180</option>
              </select>
            </div>
            <button class="button button-primary full" type="submit">Подобрать узел</button>
          </form>

          <aside class="calc-result" id="calcResult" aria-live="polite">
            <h3>Результат подбора</h3>
            <p class="calc-empty">Заполните параметры проёма и нажмите «Подобрать узел».</p>
          </aside>
        </div>
      </section>

      <section class="section section-light">
        <div class="container">
          <h2>Как монтируется узел ФП-БУСТ-ПКМ-01</h2>
          <ol class="howto">
            <li><strong>Минплита.</strong> Свободное пространство проёма заполняется фрагментами минераловатных плит плотностью ≥150 кг/м³.</li>
            <li><strong>Пена ФП-БУСТ-01.</strong> Пространство вокруг кабелей и шинопроводов заполняется на всю глубину заделки.</li>
            <li><strong>Наружные швы.</strong> Швы плит и примыкания к проёму и коммуникациям обрабатываются герметиком.</li>
            <li><strong>Финишный слой ФП-БУСТ-05.</strong> Абляционный слой ≥1 мм наносится с обеих сторон проходки.</li>
            <li><strong>Эстетика узла.</strong> Подрезка и затирка поверхности для чистого внешнего вида.</li>
          </ol>
        </div>
      </section>
"""
    out = ROOT / page["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head(page) + breadcrumbs(page) + body + footer(), encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def write_sitemap(slugs) -> None:
    urls = [f"{BASE}/"] + [f"{BASE}/{s}/" for s in slugs]
    items = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <changefreq>monthly</changefreq>\n"
        f"    <priority>{'1.0' if u == BASE + '/' else '0.8'}</priority>\n  </url>"
        for u in urls
    )
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f"{items}\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(sm, encoding="utf-8")
    print("wrote sitemap.xml with", len(urls), "urls")


def main() -> None:
    for page in PRODUCT_PAGES:
        render_product(page)
    render_calculator()
    slugs = [p["slug"] for p in PRODUCT_PAGES] + ["kalkulyator"]
    write_sitemap(slugs)


if __name__ == "__main__":
    main()
