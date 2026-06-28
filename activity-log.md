# Activity log

- 2026-06-28 22:04 - Created project folder outside OneDrive at `C:\Users\aleks\Documents\Codex\fp-boost-pkm-landing`.
- 2026-06-28 22:05 - Confirmed source PDF exists at `C:\Users\aleks\Downloads\2026 Комплект документации проходки ФП-БУСТ-ПКМ-01.pdf`.
- 2026-06-28 22:06 - Checked PDF metadata: 86 pages, 1024 x 768 pt presentation format, created with PDF24.
- 2026-06-28 22:09 - Rendered all 86 PDF pages to `assets\pdf-pages` as JPEG assets for the landing page.
- 2026-06-28 22:16 - Copied the original PDF to `assets\fp-boost-pkm-01-documentation.pdf` for download from the site.
- 2026-06-28 22:19 - Generated `content.json` with page metadata, source images, section groups, and extracted searchable text.
- 2026-06-28 22:30 - Built the landing page files: `index.html`, `styles.css`, `script.js`, and reproducible `tools\build_content.py`.
- 2026-06-28 22:36 - Added `server.mjs` and switched local preview from Python `http.server` to a stable Node static server.
- 2026-06-28 22:39 - Verified in Chrome headless: 86 page cards render on desktop and mobile, modal preview opens, images load, no console or request errors, no horizontal overflow.
- 2026-06-28 22:55 - Studio redesign: rebuilt landing into a selling B2B page. Added sales structure (offer-driven hero, trust strip, problem/solution, advantages, animated stats, audience, process, reviews, FAQ, contacts + lead form, sticky mobile CTA). Switched font to Manrope, added OG/JSON-LD/SVG favicon. Contacts are placeholders. Verified in Chrome (DevTools MCP): no console errors, no horizontal overflow, counters animate, lead form validates + auto-formats phone + shows success state.
