# Mock POWER UP kickoff — facilitator guide

**What it is:** a tabletop kickoff drill for TAS. The **game and field** are FIRST POWER UP (2018); the **pit** builds to **2026 construction rules**, with the **2027 Part 1** preview as a watch list. Students get the **Game Manual–style PDF**; mentors use this guide only.

| File | Use |
| --- | --- |
| `mock-kickoff-2018-packet.pdf` | **Student handout** (~60 Letter pages). |
| `mock-kickoff-2018-packet.md` | Source; edit then regenerate PDF. |
| `mock-kickoff-2018-packet-outline.md` | Section outline and page estimates. |
| `mock-kickoff-2018-usage.md` | **This file** — do not hand to students. |

## Student manual map (use these section names)

| Topic | Packet location |
| --- | --- |
| Cover, TOC, which rules apply | Front matter FM.1–FM.4 |
| Animation | Vol I §1.2 (`HZbdwYiCY74`) |
| Field tour | Vol I §3 ARCADE |
| Scoring / POWER UPS | Vol I §4 (Tables 4-1, 4-2) |
| **2018 match envelope** (R03, G05/R04, R05) | Vol I §5 |
| Game rules (G-series) | Vol I §6 |
| **2026 construction** (motors, wire, bumpers) | Vol II §7–8 |
| 2027 preview | Vol III §9 |
| AprilTag fiction | Appendix B |
| Homework / study sheets | Appendix D |

## Common facilitator mistake — 2026 match limits (R107 / R105)

The student manual **deliberately omits** 2026 **R107** (30 in match height) and **R105** (12 in horizontal extension). If you apply those rules to POWER UP play, Scale placement and rung climbs become illegal and the mock breaks. **Only mention R107/R105 here, in this guide** — when a student imports “today’s FRC rules” into the game, stop them, point to Vol I §5 and FM.2, and say: *“Construction is 2026; the game on the field is still 2018.”*

## Who and when

- **Facilitator:** one mentor or lead student.
- **Audience:** full team or new members; 6–30 people.
- **Short (10–15 min):** disclaimer, animation, Vol I §5 one-liner, two prompts.
- **Full (75–90 min):** walk Vol I §3–§4, skim Vol II §8, Vol III §9, optional Appendix B for vision.

## Short script

**Frame:** “TAS mock kickoff — 2018 field, 2026 pit, not real 2027 rules.”

**Video:** [2018 POWER UP animation](https://www.youtube.com/watch?v=HZbdwYiCY74) full screen.

**Rules line:** Open **Vol I §5**. Board: **R03 55 in · G05/R04 16 in · R05 120 lb**. Do **not** put 2026 match-size rules on the board.

**Close:** Hand out PDF; homework **Appendix D.3** using §5 limits.

## Full run-of-show (optional)

| Phase | Time | Packet |
| --- | ---: | --- |
| Cover + FM.2 | 5 min | Which rules apply |
| Video | 4 min | §1.2 |
| Field | 20 min | §3 |
| Scoring | 15 min | §4 |
| Match envelope | 10 min | §5 |
| Construction skim | 10 min | Vol II §8 |
| 2027 preview | 8 min | Vol III §9 |
| Tags (optional) | 10 min | Appendix B |
| Close | 5 min | Appendix D.7 |

## What not to do

- Don’t apply **R107/R105** to student play (see above).
- Don’t present Appendix B as real field hardware.
- Don’t re-host FIRST video or full manuals — link only.
- Don’t post the packet publicly.

## Regenerate PDF (tashpc)

```bash
cd docs  # or /cursor/stores/self/docs
PANDOC=$(python3 -c "import pypandoc; print(pypandoc.get_pandoc_path())")
$PANDOC mock-kickoff-2018-packet.md -f markdown+raw_html -t html5 -s \
  --metadata pagetitle="TAS Mock FRC Game Manual — POWER UP 2018" \
  --css mock-kickoff-2018-packet.css --embed-resources -o /tmp/mock-packet.html
python3 -m weasyprint /tmp/mock-packet.html mock-kickoff-2018-packet.pdf
```

*Facilitator guide · V0 · 2026-11-09 · see `mock-kickoff-2018-changelog.md`*
