from __future__ import annotations

import json
import re
from pathlib import Path

import pdfplumber


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = sorted((Path.home() / "Downloads").glob("2026*.pdf"))[0]

SECTION_RANGES = [
    (1, 1, "cover", "Обложка и состав комплекта"),
    (2, 2, "product", "Типы огнестойких проходок"),
    (3, 3, "materials", "Материалы для монтажа"),
    (4, 5, "stages", "Стадии работ"),
    (6, 7, "details", "Типовой узел и принцип действия"),
    (8, 10, "factory", "Заводские решения"),
    (11, 12, "variants", "Вариации монтажа"),
    (13, 20, "portfolio", "Портфолио и примеры работ"),
    (21, 30, "certificates", "Сертификаты соответствия"),
    (31, 86, "manual", "Технологический регламент по монтажу"),
]


def section_for(page_num: int) -> dict[str, str]:
    for start, end, key, title in SECTION_RANGES:
        if start <= page_num <= end:
            return {"key": key, "title": title}

    return {"key": "other", "title": "Документация"}


def clean_text(raw: str) -> str:
    raw = (raw or "").replace("\x00", " ")
    lines = []
    for line in raw.splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def make_summary(text: str) -> str:
    compact = re.sub(r"\s+", " ", text or "").strip()
    return compact[:420]


def page_title(page_num: int, section: dict[str, str]) -> str:
    if section["key"] == "manual":
        return f"Технологический регламент: лист {page_num - 30}"
    if section["key"] == "certificates":
        return f"Сертификаты соответствия: лист {page_num - 20}"
    return section["title"]


def main() -> None:
    pages = []
    with pdfplumber.open(SOURCE_PDF) as doc:
        for idx, page in enumerate(doc.pages, 1):
            text = clean_text(page.extract_text(x_tolerance=1, y_tolerance=3) or "")
            section = section_for(idx)
            pages.append(
                {
                    "number": idx,
                    "title": page_title(idx, section),
                    "section": section["key"],
                    "sectionTitle": section["title"],
                    "image": f"assets/pdf-pages/page-{idx:02d}.jpg",
                    "text": text,
                    "summary": make_summary(text),
                }
            )

    content = {
        "sourcePdf": "assets/fp-boost-pkm-01-documentation.pdf",
        "pageCount": len(pages),
        "sections": [
            {"key": key, "title": title, "start": start, "end": end, "count": end - start + 1}
            for start, end, key, title in SECTION_RANGES
        ],
        "pages": pages,
    }

    (PROJECT_ROOT / "content.json").write_text(
        json.dumps(content, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote content.json with {len(pages)} pages from {SOURCE_PDF}")


if __name__ == "__main__":
    main()
