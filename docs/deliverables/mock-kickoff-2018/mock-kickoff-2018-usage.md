# Mock POWER UP kickoff — facilitator guide (TAS-MOCK-V1)

**Not for students.** Points at the 2018-clone student PDF (`mock-kickoff-2018-packet.pdf`).

## Student manual map

| Topic | Section |
| --- | --- |
| Animation | §1.2 (`HZbdwYiCY74`) |
| Field tour | §3 ARCADE |
| Scoring / POWER UPS | §4 (Tables 4-1, 4-2) |
| **2018 match envelope** (R03, G05/R04, R05) | §8.2 (also G05 in §7.2) |
| Game rules (G-series) | §7 |
| **2026 construction** | §8 |
| 2027 preview | §1.7 mock Team Update |
| AprilTag fiction | Appendix B |
| Quizzes / homework | This guide only — not in student PDF |

## Common facilitator mistake — R107 / R105

The student manual **omits** 2026 **R107** and **R105**. If applied to POWER UP, Scale placement and rung climbs break. Mention them only here; point students to **§1.5** and **§8.2** and say: *"Construction is 2026; the game on the field is 2018."*

## Short script

1. Read cover disclaimer aloud.
2. Play animation (§1.2).
3. Board line: **R03 55 in · G05/R04 16 in · R05 120 lb** (from §8.2 / §7.2).
4. Two prompts: best SWITCH strategy? how many motors for climb + elevator (§8.5 + §1.7 TU)?

## Regenerate PDF

```bash
cd /home/jovyan/work/docs/mock-kickoff-2018
pandoc mock-kickoff-2018-packet.md -f markdown+raw_html -t html5 -s -o /tmp/mock-packet.html
python3 -m weasyprint /tmp/mock-packet.html mock-kickoff-2018-packet.pdf -s mock-kickoff-2018-packet.css
```

*TAS-MOCK-V1 · 2026-11-09*
