"""Curate and web-optimize the best embedded PDF images into assets/img/.

Picks real installation photos, branded product shots, object photos and
high-resolution certificate scans (far cleaner than the slide-page screenshots),
then resizes + recompresses them for the landing page.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "assets" / "extracted"
OUT = PROJECT_ROOT / "assets" / "img"

# out_name -> (source_file, max_width, quality)
JOBS = {
    "materials.jpg":  ("p07-x426.jpeg", 1200, 82),   # branded F.P.BOOST product boxes + sealant
    "work-1.jpg":     ("p04-x345.jpeg", 1200, 82),   # installer fitting penetration (human, dynamic)
    "work-2.jpg":     ("p10-x485.jpeg", 1200, 82),   # applying sealant to node
    "node.jpg":       ("p06-x399.jpeg", 1600, 84),   # wide cable-penetration cross section
    "factory-1.jpg":  ("p08-x447.jpeg", 1100, 82),   # wrapped mineral-wool boards
    "factory-2.jpg":  ("p09-x462.jpeg", 1100, 82),   # red product line boxes
    "factory-3.jpg":  ("p10-x489.jpeg", 1100, 82),   # ready foam block
    "object-1.jpg":   ("p13-x544.jpeg", 1300, 84),   # glass business tower
    "object-2.jpg":   ("p11-x511.jpeg", 1300, 84),   # modern faceted facade (telecentre)
    "object-3.jpg":   ("p13-x556.jpeg", 1100, 84),   # courtyard / residential complex
    "object-4.jpg":   ("p13-x548.jpeg", 1100, 84),   # aerial campus view
    "cert-1.jpg":     ("p21-x749.jpeg", 1100, 80),   # certificate scan (hi-res)
    "cert-2.jpg":     ("p25-x769.jpeg", 1100, 80),   # certificate scan (hi-res)
    "cert-3.jpg":     ("p26-x774.jpeg", 1100, 80),   # appendix scan
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for out_name, (src_name, max_w, q) in JOBS.items():
        src = SRC / src_name
        if not src.exists():
            print(f"!! missing {src_name}")
            continue
        im = Image.open(src)
        im = ImageOps.exif_transpose(im).convert("RGB")
        if im.width > max_w:
            h = round(im.height * max_w / im.width)
            im = im.resize((max_w, h), Image.LANCZOS)
        dst = OUT / out_name
        im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
        kb = dst.stat().st_size // 1024
        print(f"{out_name:<14} {im.width}x{im.height:<5} {kb}KB  <- {src_name}")


if __name__ == "__main__":
    main()
