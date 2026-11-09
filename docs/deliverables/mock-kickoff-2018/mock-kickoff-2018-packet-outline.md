# TAS mock FRC Game Manual — section outline (V0, 2026-11-09)

Source file: `docs/mock-kickoff-2018-packet.md`. Styles: `docs/mock-kickoff-2018-packet.css` (Letter, WeasyPrint).
Page estimates assume pandoc → HTML → WeasyPrint at 10 pt, with the forced `page-break` divs in the source. Expected total is **about 32 pages (range 28–38)**.

| # | Section | Contents | Est. pages |
| --- | --- | --- | ---: |
| — | Cover (`cover-page`) | Watermark banner "TAS MOCK · HYPOTHETICAL · NOT OFFICIAL", title, volume list, meta, disclaimer | 1 |
| — | Contents | Mock notice + nested TOC with section numbers | 1 |
| FM | Front matter | FM.1 About; FM.2 Which rules apply (Table FM-1, design-target note); FM.3 Conventions (rule-box sample, ID scheme, figure placeholder, fiction marking, running headers); FM.4 Sources and legal (Table FM-2) | 3 |
| I-1 | Vol I Sec 1 Introduction | Kickoff story; official animation box (YouTube `HZbdwYiCY74`, watch + embed URLs); how to use Vol I (map to 2018 sections) | 1.5 |
| I-2 | Vol I Sec 2 Overview | Periods, FMS plate randomisation, Table 2-1 points, ranking points, three strategy questions | 1 |
| I-3 | Vol I Sec 3 ARCADE | 3.1 zones (Table 3-1); 3.2 field; 3.3 SCALE (Table 3-2 states, RUNG, BRICKS, PLATFORM); 3.4 SWITCH (Table 3-3, FENCE, 9 vs 18.75 in. note); 3.5 lighting; 3.6 alliance wall / EXCHANGE / VAULT; 3.7 PORTAL; 3.8 cube; 3.9 vision targets (+ fiction reminder); 3.10 FMS; 8 figure placeholders | 4.5 |
| I-4 | Vol I Sec 4 MATCH play | 4.1 stages and cube staging; 4.2 OWNERSHIP + Table 4-1 rewards; 4.3 Table 4-2 POWER UPS + queue rules + timeline placeholder; 4.4 Table 4-3 penalties; 4.5 Table 4-4 drive team; 4.6 logistics | 3.5 |
| I-5 | Vol I Sec 5 Match envelope | FRAME PERIMETER; rule boxes R03, R04, G05, R05; read-together note; design implications; Table 5-1 | 2.5 |
| I-6 | Vol I Sec 6 Game rules | Rule boxes G01, G03, G04, G05–G09, G10–G18 (incl. pins, NULL TERRITORY, PLATFORM ZONE), G19–G25, A01–A04; contact summary; design consequences | 5 |
| II-7 | Vol II Sec 7 Overview | Precedence, the single neutral line on 2026 match-size rules, Table 7-1 | 1 |
| II-8 | Vol II Sec 8 Construction | 8.1 R103; 8.4 bumpers Table 8-A (R401–R412); 8.5 R501/R502/R503 boxes, controllers context, motor budget; 8.6 R601 box + R602/R605–R609; 8.7 Table 8-B R701–R717; 8.8 Table 8-C pneumatics; 8.9 console pointer (R901–R907) | 5 |
| III-9 | Vol III Sec 9 2027 Part 1 | Table 9-1 seven verified bullets; what Part 1 does not say; TAS implications; Table 9-2 three-layer snapshot | 2 |
| A | Appendix A | Table A-1 precedence by topic; Table A-2 rule-ID index | 1.5 |
| B | Appendix B (FICTION) | Fiction call-out; Table B-1 allocation; B.1–B.4 tag tables IDs 1–32; B.5 known limitations | 2.5 |
| C | Appendix C Glossary | Table C-1 game terms (2018); Table C-2 construction terms (2026) | 2 |
| D | Appendix D Study sheets | D.1 scoring worksheet; D.2 20-question quiz; D.3 design checklist; D.4 motor budget; D.5 AUTO planner; D.6 rule-lookup drill; D.7 mentor checklist; D.8 answer key | 4 |
| E | Appendix E Revision history | V0 2026-11-09; closing mock notice; end mark | 0.5 |
| | **Total** | | **≈ 32** |

## Constraint checks (run on the source)

- `grep -nE "R10[57]" docs/mock-kickoff-2018-packet.md` → no hits.
- 2026 match-size rules are mentioned once, in the neutral line at the top of Vol II Sec 7; R104/R106 are not cited.
- YouTube `HZbdwYiCY74` appears in Sec 1.2 (watch and embed) and in the D.7 checklist.
- 2018 envelope rules R03, R04, R05 and G05 have rule boxes and cite the 2018 PDF URL.
- 2027 bullets match the Part 1 blog text (18 motors; E510-like heat/cool rule; pneumatics unchanged; CANivore on Systemcore for 2027; original Talon and Victor SP removed; BAG/Mini-CIM off the explicit list, 20 A or less only; USB ≤ 100 Wh).

## Build notes for Composer

- Front matter uses `pagetitle:` (not `title:`) so pandoc does not print a title block above the cover.
- All `##` headings carry `{.no-counter}` because the source numbers sections explicitly; without it the CSS `h2::before` counter would prefix a second number.
- Appendix `#` headings carry `{.appendix-header}`.
- Rule boxes, cover, figure placeholders and notices are raw HTML using the existing CSS classes (`cover-page`, `cover-banner`, `rule-box`, `rule-id`, `rule-violation`, `rule-source`, `vol-banner`, `figure-box`, `page-break`, `mock-notice`, `fiction`, `toc`, `watermark-repeat`).
- `mock-kickoff-2018-usage.md` still cites the old handout's section numbers (§2 envelope, §3 build, §4 2027, §6 tags, §7 diff, §8 checklist). Those now map to Vol I Sec 5, Vol II Sec 7–8, Vol III Sec 9, Appendix B, Table 9-2 and Appendix D.7. The usage guide was not edited, as instructed.
