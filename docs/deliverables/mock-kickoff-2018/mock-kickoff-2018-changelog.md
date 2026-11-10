# Changelog — mock kickoff 2018 packet

## TAS-MOCK-V1.2 — reliable PDF build (embedded figures)

- Added `build_packet_pdf.sh` (fixed cwd + pandoc `--resource-path`) and `verify_packet_pdf.py`.
- Root cause: WeasyPrint from wrong directory → captions render, **no** `figures/` embeds (~170 KB PDF).
- Rebuilt PDF with all official manual JPEGs + tagged overlays.

## TAS-MOCK-V1.1 — official diagram JPEG extracts; fiction AprilTag overlays on §3 + Appendix B
TAS-MOCK-V1 (2026-11-09)

- Restructured to official **2018 manual §1–§11** layout (no Vol I/II/III).
- White cover, Arial/blue typography per template spec.
- Match envelope (R03–R05, G05) under **§8.2**; game rules **§7**.
- **2026 §8** construction graft; **§1.7** mock Team Update for 2027 Part 1.
- Removed facilitator study appendices from student PDF.
- PDF: 46 pages (WeasyPrint, Letter).

## V0 (2026-11-09) — superseded

- Three-volume custom layout; rejected for not matching 2018 manual clone.
