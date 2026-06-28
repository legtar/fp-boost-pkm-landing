"""Extract embedded raster images from the source PDF in their original quality.

Slide-page renders (assets/pdf-pages) include borders, captions and compression.
The underlying embedded photos/diagrams are cleaner and higher-resolution, which is
what we want for a polished landing. This dumps every embedded image with metadata
so the best ones can be curated into assets/extracted/.
"""
from __future__ import annotations

import json
from pathlib import Path

import fitz  # PyMuPDF

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = sorted((Path.home() / "Downloads").glob("2026*.pdf"))[0]
OUT_DIR = PROJECT_ROOT / "assets" / "extracted"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(SOURCE_PDF)
    catalog = []
    seen_xrefs: dict[int, str] = {}

    for page_index in range(len(doc)):
        page = doc[page_index]
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen_xrefs:
                catalog.append({
                    "page": page_index + 1,
                    "xref": xref,
                    "file": seen_xrefs[xref],
                    "duplicate": True,
                })
                continue
            try:
                base = doc.extract_image(xref)
            except Exception as exc:  # noqa: BLE001
                catalog.append({"page": page_index + 1, "xref": xref, "error": str(exc)})
                continue

            ext = base.get("ext", "png")
            width = base.get("width", 0)
            height = base.get("height", 0)
            name = f"p{page_index + 1:02d}-x{xref}.{ext}"
            (OUT_DIR / name).write_bytes(base["image"])
            seen_xrefs[xref] = name
            catalog.append({
                "page": page_index + 1,
                "xref": xref,
                "file": name,
                "ext": ext,
                "width": width,
                "height": height,
                "bytes": len(base["image"]),
                "colorspace": base.get("colorspace"),
            })

    (OUT_DIR / "_catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    uniques = [c for c in catalog if c.get("file") and not c.get("duplicate")]
    print(f"Extracted {len(uniques)} unique images from {len(doc)} pages -> {OUT_DIR}")


if __name__ == "__main__":
    main()
