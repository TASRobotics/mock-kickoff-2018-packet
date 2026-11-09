---
cursor:
  subagentId: "bc-cc232e07-91d9-52fe-b5ea-74d8413d2bdd"
---
# Mock FRC kickoff: POWER UP 2018 field, 2026 robot rules, 2027 updates (scope, 2026-11-09)

Allan's ask: a mock kickoff where the **game and field are FIRST POWER UP (2018)**, the **robot construction rules are 2026 (REBUILT)**,
and **2027 rule changes** are layered on as FIRST reveals them. Kickoff feel follows the 2018 kickoff (game video + introduction), with
the copy rewritten for modern robots. Vision is a **TAS AprilTag retrofit** of the 2018 field, including tags on the scale plates so a robot
can read the scale's height at a given time. **Audience: TAS only** (tashpc `:8050` on campus LAN; no public publish).

**No production UI until Allan approves the wireframe in section 8.** No new dirs under `s6e8/` or `ptcg/`; all code lives in
`RaidZero-Simulation` (`mechanism-sim/` + `aprilsim/`).

Inputs read: `mechanism-sim/public/spa/field-overlays/powerup-2018.json`, `mechanism-sim/src/spa/game/sideViewGame.ts`,
`aprilsim/season.py`, `aprilsim/field.py`, `aprilsim/sim.py`, `aprilsim/retro.py`, `docs/mechsim-game-height-limits-audit-20261103.md`,
`docs/game-selector-overlay-vs-limits-20261102.md`, the 2018 Game Manual
([PDF](https://firstfrc.blob.core.windows.net/frc2018/Manual/2018FRCGameSeasonManual.pdf)), the 2026 Game Manual TU22
([PDF](https://firstfrc.blob.core.windows.net/frc2026/Manual/2026GameManual.pdf)) and the two FIRST 2027 preview blogs.

## 0. The headline design finding

Literal 2026 robot rules make most of POWER UP's vertical game illegal. 2026 **R107** caps total height at **30 in** with no endgame or
climb exception (G413 exceptions are damage / momentary only); **R105** is 12 in past the perimeter and **R106** one side at a time.

| 2018 target | Height | Under 2026 R105-R107 (defaults D1 + D2) |
| --- | --- | --- |
| Exchange lower opening | 0-16.25 in, 1.75 in ramp | Reachable |
| Portal / Exchange return (intake) | 20-34 in opening | Reachable (intake at 20-30 in) |
| Platform (park) | 3.5 in, 15.35 deg ramps | Reachable |
| Switch plate | 9 in level, behind an **18.75 in fence** | **Reachable if the held cube does not count toward R107** (cube carried on a tray at <= 30 in clears the fence). If it counts: marginal (cube bottom 19 in, 0.25 in over the fence), toss only |
| Scale plate | 48-72 in edge | **Not placeable**; launch only |
| Rung (climb) | top at **84 in**, 8.25 in off the tower face | **Impossible** by climbing; only LEVITATE (vault power-up = free climb) scores it |

The strategy shifts to exchange / vault / switch, with the scale as a launch target **only if** someone applies 2026 in-match size rules.
That tension is a **facilitator teaching tangent**, not the student manual.

**Kickoff packet default (Allan, 2026-11-09):** student-facing `mock-kickoff-2018-packet.pdf` uses **2018 match envelope** (R03, G05/R04,
R05) plus **2026 construction** (Vol II). **No R107/R105 in the student PDF.**

- ~~**Option L (literal 2026 R-rules in-match):** struck for the kickoff deliverable~~ — do not hand students a literal-2026-match reading
  of POWER UP.
- **Option M (mock-GDC override):** optional for a future sim/UI only (explicit override rows in data, section 6), not for the paper kickoff.

## 1. Defaults to confirm (one word each)

This folds every open question from the earlier draft into one list. Reply with the numbers to change; anything not mentioned ships as
the default.

| # | Decision | Recommended default | Alternative |
| --- | --- | --- | --- |
| D1 | Rule mode | **2018 match envelope + 2026 construction** (packet default; see `mock-kickoff-2018-packet.pdf`) | M (mock-GDC overrides on, sim only) |
| D2 | Held POWER CUBE counts toward a 30 in cap | **N/A for packet** (2018 has no such cap; R107 not in student doc) | Facilitator tangent only |
| D3 | Kickoff entry point | **Own route chip** `#/kickoff` | Entry inside the Game pill menu |
| D4 | 2027 previews in the diff table | **Motor cap (18) gets a row; the other bullets are footnotes** | Every bullet as a row |
| D5 | Kickoff video | **Embed the official FIRST 2018 game animation (YouTube) with a link-out fallback**; no re-hosting | Link-out only |
| D6 | Vision for the mock game | **AprilTag retrofit, 20 tags (16 static + 4 on the scale plates)**, section 4 | Fewer static tags (scale + switch only) |
| D7 | Real 2018 profile vision (`powerup-2018`, not the mock) | **Fix to `retro`** (manual 3.9 switch-fence tape) | Leave `none` |
| D8 | Scale tag mounting | **Hanging panel under each plate's outer end, one tag facing each alliance (4 tags)** | One tag per plate on the plate's side face |
| D9 | Scale height over time | **MVP: one scale state per run** (red-owned / level / blue-owned / custom angle); a time schedule comes later | Time schedule in MVP |
| D10 | aprilsim 2018 season | **In MVP** (SeasonSpec + layout + field image + 3 season-neutral drives) | Phase 2 |
| D11 | Plate colour randomisation (FMS game data) | **Off** (fixed assignment) | Scenario knob |
| D12 | Hosting | **TAS only**: tashpc `:8050` campus LAN; no `publish-app`, no public deploy | (none; public is out of scope) |
| D13 | 2018 field artwork | **WPILib/PathWeaver 2018 field image**, cropped into the layout's `field-image` block | Hand-drawn top-down from the manual dimensions |

## 2. MVP (smallest shippable kickoff experience on combined `:8050`)

Combined mode today: `python3 -m aprilsim web --port 8050 --mech-spa <dist>` serves the mech SPA at `/` and AprilTag at `/apriltag/`
(`aprilsim/web/server.py` `MECH_SPA`). The aprilsim side of the MVP has to change, because the AprilTag route only knows `2025` and `2026`.

**MVP-A, mech SPA (static bundle):**

1. **Kickoff page `#/kickoff`** (section 3): video, introduction, rule reveal, reachability board, "Open the sim" links.
2. **New Game entry `mock-2018-r2026`** in the top-bar Game selector: label "POWER UP field · 2026 robot rules", `vision: 'tag'`. It
   reuses the `powerup-2018` field overlay and composes limits from the 2026 rule pack (section 6). Every mechanism page that already honours
   the Game profile (double arm, elevator, telescoping, orbit, single-arm readout; see the limits audit) then gives 2026 verdicts on 2018
   targets, including the start-limit freeze.
3. **Overlay fixes and missing elements** from section 7 that the board needs: platform, rung, switch neutral state, exchange ramp.
4. **2027 layer as a list, not physics**: preview deltas in the diff table with status `preview` and source link; the 18-motor cap is a
   count only (no enforcement until a robot-wide motor inventory exists).

**MVP-B, aprilsim (section 4):**

5. `SeasonSpec("2018")` + layout `2018-powerup-tas-retrofit.json` (20 tags) + field image, `VISION_BY_YEAR["2018"] = "tag"` for the
   mock season.
6. Scale state knob: the `true` layout gets the tilted scale tags, the `believed` layout stays level (the split already exists in
   `sim.py`). Output adds an estimated scale edge height next to the true one.

Out of MVP: scoring / match sim, scale time schedule, plate-colour randomisation, cycle-time estimator, retro-tape pipeline for the real
2018 profile (only its `vision` flag is fixed, D7).

## 3. Kickoff UX (2018 kickoff vibe, modern copy)

The 2018 kickoff pattern was: game animation, then hosts walking through the field elements, then the rules and season changes. The mock
follows the same order on one `#/kickoff` page, each block a full-width card:

1. **Cold open**: the official FIRST POWER UP game animation, embedded from FIRST's YouTube (D5). Below it, one line: "TAS mock kickoff ·
   FIRST POWER UP field · built to 2026 robot rules."
2. **Welcome card** (copy draft): "It's 2018 on the field and 2026 in the pit. You have the POWER UP game you know (switch, scale,
   exchange, vault, climb) and the robot rules you build to today: 115 lb, 110 in perimeter, 30 in tall, 12 in past your frame, one side at a
   time. Figure out what's still worth doing."
3. **Field tour**: five element cards (Switch, Scale, Exchange + Vault, Power Ups, Platform + Rung) in the 2018 order. Each card has the
   2018 numbers and a red/amber/green strip "under 2026 rules" taken from the reachability board, so the tour is the reveal.
4. **What's new for your robot**: the rule diff table (section 6), with the 2027 preview footnotes and an empty **Team Update feed**
   ("Mock TU 00 · posted at kickoff"). Real 2027 Team Updates append here as FIRST publishes them (TU 00 arrives with the January 2027
   manual); mock overrides (Option M) show with a "mock" badge.
5. **Vision card**: "This field has AprilTags now." Top-down field with the 20 tag dots, scale plates highlighted, and a link to the
   AprilTag route preloaded with season 2018.
6. **Open the sim**: buttons for Elevator / Orbit / Double arm / AprilTag, each opening with Game = `mock-2018-r2026`.

Copy rules: name rule ids (R105, R107) the way the pages already do; say "mock" wherever the rule is ours rather than FIRST's; link FIRST
manuals and blogs, never re-host them (TAS-only does not change that).

## 4. aprilsim season `2018` and the TAS AprilTag retrofit

### 4.1 `SeasonSpec("2018")`

Add to `SEASONS` in `aprilsim/season.py` (fields as in the dataclass today):

```python
"2018": SeasonSpec(
    id="2018",
    layout="2018-powerup-tas-retrofit",
    andymark="2018-powerup-tas-retrofit",      # one physical variant; the 2025/2026 welded vs AndyMark split does not exist
    default_drive="stop_and_go",
    allowed_drives=frozenset({"fast_travel", "spin_drive", "stop_and_go"}),  # season-neutral; hub-aim drives are 2026-only
    tag_filters=("all", "static", "switch", "scale_tower", "exchange_portal", "scale_plates"),
    hubs=(),
    bumps_allowed=False, hub_blocks_allowed=False, netting_allowed=False,
    holdout_label="2018 retrofit holdout",
    scenario_defaults=dict(_DEFAULTS_2018),
    scenario_ranges=dict(_RANGES_2018),
),
```

- `_DEFAULTS_2018`: `robot_height 0.70`, `camera_height 0.60`, `auto_tilt True`, `other_robots 5`, `tall_robots 0`, `tall_height 0.762`,
  lighting knobs as 2025 (soft). Every robot on the field obeys R107, so `_RANGES_2018` caps `robot_height` and `tall_height` at
  **0.762 m** and `camera_height` at **0.74 m**.
- `retro.py` `VISION_BY_YEAR["2018"] = "tag"` (the mock season). The mech SPA keeps the real `powerup-2018` profile at `retro` (D7) and gives
  `mock-2018-r2026` `tag`, so the history stays true and the mock gets tags.
- `drive_options_for` / `tag_filter_options_for` need labels for the new filter ids; `schema_season_meta()` picks up the season
  automatically. Phase 2 drives: `exchange_switch_cycle`, `orbit_stress_scale`.
- `field_payload()` needs a `scale` marker list for the preview (plates + tower AABBs), alongside the existing `hubs` / `reefs`.

### 4.2 Layout `aprilsim/layouts/2018-powerup-tas-retrofit.json`

WPILib layout format as the 2025/2026 files (`name`, `season`, `game`, `field-image`, `field-dimensions`, `program`, `field-tags`), so
`FieldLayout.load` reads it unchanged. 36h11 tags at `TAG_SIZE` 6.5 in (8.125 in with border).

Frame: WPILib convention, origin at the blue alliance wall, +x toward red, y across the field. Field **16.459 x 8.230 m**
(54 x 27 ft, manual 3.1), centre line y = 4.115. Element positions from the manual: switch centres 14 ft from each alliance wall
(x = 4.267 / 12.192), switch fence 4 ft 8 in deep (faces at x = 3.556 / 4.978 and 11.481 / 12.903), scale centred (x = 8.229), scale
plates 3 x 4 ft with outer edges 15 ft apart (plate x 7.620-8.839, y 1.829-2.743 and 5.487-6.401). Yaw 0 = tag faces +x (toward red).

| IDs | Where | x [m] | y [m] | z [m] | Yaw | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1, 2 | Blue switch, blue-facing fence | 3.556 | 2.797, 5.433 | 0.30 | 180 | Where the 2018 retro tape was (±51 7/8 in from switch centre); fence top 0.476 m |
| 3, 4 | Blue switch, scale-facing fence | 4.978 | 2.797, 5.433 | 0.30 | 0 | |
| 5, 6 | Red switch, scale-facing fence | 11.481 | 2.797, 5.433 | 0.30 | 180 | |
| 7, 8 | Red switch, red-facing fence | 12.903 | 2.797, 5.433 | 0.30 | 0 | |
| 9, 10 | Exchange walls (blue, red) | 0 / 16.459 | **TBD** (between player stations 1 and 2, field drawing) | 1.00 | 0 / 180 | Above the return (opening top 0.864 m) |
| 11-14 | Portal walls (4 corners) | **TBD** | **TBD** | 1.00 | wall normal, **TBD** | Above the 14 in opening (top 0.864 m); angles from the field drawings |
| 15, 16 | Scale tower faces (toward blue, toward red) | 8.229 ∓ tower half-depth (**TBD**) | 4.115 | 0.90 | 180 / 0 | Fixed reference near the scale |
| 17-20 | **Scale plates, moving** (section 4.3) | 7.620 / 8.839 | 1.979 / 6.251 at level | 1.374 at level | 180 / 0 | 17: low-y plate facing blue, 18: low-y facing red, 19: high-y facing blue, 20: high-y facing red |

TBD rows need the 2018 field drawings (layout and marking diagram); they are not in the manual text. Tags 1-16 are `static`; 17-20 are
`scale_plates`. The layout's `field-tags` list them at the level pose, so every existing loader works. An extra top-level block, ignored by
`FieldLayout.load`, carries the motion:

```json
"tas-dynamic": {
  "scale": {
    "tags": [17, 18, 19, 20],
    "pivot": {"x": 8.229, "y": 4.115, "z": 1.524},
    "axis": "x",
    "edgeRadiusM": 2.286,
    "statesEdgeIn": {"ownedLow": [48, 56], "level": [56, 64], "opponentHigh": [64, 72]},
    "src": "2018 manual 3.3.2; pivot height = level plate surface (verify vs drawing TE-18007)"
  }
}
```

### 4.3 Scale-plate tag spec (the retrofit that reads scale height)

- **Mount**: a rigid panel hanging under each plate's outer end, fixed to the plate so it tilts with it. Tag centre **0.15 m below the plate
  surface plane** and **0.15 m inboard of the outer edge** (lateral distance d = 2.136 m from the pivot), so the whole 8.125 in tag stays
  under the plate. One tag faces each alliance wall (D8). The 3.5 in plate walls are too short for a tag, which is why it hangs below.
- **Motion**: one scalar tilt θ (rotation about +x through the pivot) moves all four tags: high-y plate up for θ > 0, low-y plate down.
  Pose(θ) = R_x(θ) applied about the pivot to the level pose. The tag stays facing ±x and rolls in its own plane by θ, so detection
  geometry barely changes and the in-plane roll plus the height both carry θ.
- **Height relation** (high-y plate; low-y uses -θ): outer edge h_e = 1.524 + 2.286 sin θ; tag centre z = 1.524 + 2.136 sin θ - 0.15 cos θ;
  y = 4.115 + 2.136 cos θ + 0.15 sin θ.

| Plate state (outer edge) | θ | Tag centre z |
| --- | --- | --- |
| 48 in (lowest owned) | -7.66 deg | 1.091 m |
| 52 in (owned, mid-band) | -5.10 deg | 1.185 m |
| 60 in (level) | 0 | 1.374 m |
| 68 in (opponent-owned, mid-band) | +5.10 deg | 1.565 m |
| 72 in (highest) | +7.66 deg | 1.660 m |

  Tag z moves about **0.037 m per degree**; the ownership band edges (56 in and 64 in at the outer edge) sit about 0.19 m apart in tag z (1.279 m vs 1.469 m).
  So a tag height error under ~5 cm classifies the state reliably, and under 2026 rules every camera sits at or below 0.74 m looking up
  0.35-0.9 m at the scale.
- **Sim use (MVP, D9)**: the run sets θ once. `true` layout = `with_moved_tags` style pose for 17-20 at θ; `believed` = level. Pose
  estimation should use `static` tags only (moving tags would bias the pose); a new readout solves θ from the 17-20 detections given the
  static-tag pose and reports estimated vs true edge height and state. `camera.py` already detects against `true_layout.corner_array`,
  so no renderer change is needed for a per-run θ.
- **Later (time schedule)**: `scale_schedule: [[t, θ], ...]` needs a per-frame true layout; `sim.py` builds `true` once today, so this is
  a new hook.
## 5. Architecture sketch

```
mechanism-sim/public/spa/
  field-overlays/powerup-2018.json      (existing, extended: platform, rung, states, ramp)   <- field geometry (gameYear)
  rules/robot-2026.json                 (NEW) R101-R107 + weight, motor, start volume         <- robotRulesYear pack
  rules/robot-2027.json                 (NEW) extends robot-2026, delta rows w/ status         <- update layer
  kickoffs/mock-2018-r2026.json         (NEW) {gameYear, robotRulesYear, updates, overrides}   <- composition
  kickoff.js                            (NEW, after mockup approval) #/kickoff route
mechanism-sim/src/spa/game/
  sideViewGame.ts + public/spa/game-profile.js   add mock-2018-r2026 (vision 'tag'); powerup-2018 vision -> 'retro'
                                                  (parity test gameProfileParity.test.ts must cover both)
  kickoffCompose.ts (NEW)                         pure: kickoff + packs -> effective rules + reachability rows
aprilsim/
  season.py                                       SeasonSpec "2018" + _DEFAULTS_2018 / _RANGES_2018 (section 4.1)
  retro.py                                        VISION_BY_YEAR["2018"] = "tag"
  layouts/2018-powerup-tas-retrofit.json (NEW)    20 tags + "tas-dynamic" scale block (section 4.2)
  field.py                                        with_scale_tilt(theta) helper next to with_moved_tags
  web/static/2018-powerup.png (NEW)               field image (D13)
```

- **Mech SPA** owns the kickoff page and the Game entry (it already has the Game bus `rz-sideview-game`, the overlay loader
  `mech-field-bridge.js`, the envelope check `checkSideViewEnvelope`, and the freeze).
- **aprilsim** owns the 2018 season, the tag layout and the scale tilt; the kickoff page links into it with season 2018 preselected.
  Both halves read numbers from JSON (layout file, `kickoffs/*.json` served under `/`) rather than code, so they cannot drift.
- **No new package.** The TS/JS duplication is already guarded by the parity test, and the JSON packs move numbers out of code.
- Tests: `kickoffCompose` vitest cases from the section 0 table; aprilsim pytest for the 2018 season (schema meta, clamp to 0.762 m,
  layout loads, θ = 0 equals level, the section 4.3 height table, θ round trip from synthetic detections).

## 6. Rule layering model

Two independent axes, composed at load time; every effective rule remembers which layer it came from.

- `gameYear` (2018) owns: field geometry, game elements, scoring, G-rules about play (zones, contact, pinning, exchange, vault), vision
  targets.
- `robotRulesYear` (2026, later 2027) owns: section-8 R-rules (perimeter, start volume, extension, height, weight, motors, electrical).
- Robot-limit rules that the old game duplicated as G-rules (2018 G05 = R04) are **replaced** by the robot pack, not merged.
- `overrides`: mock-GDC rows that change a composed rule; always shown with a "mock" badge.
- `updates`: ordered deltas on the robot pack, each with `status: preview | manual | teamUpdate` and a source URL. A `preview` row never
  changes a numeric limit until promoted to `manual`.

```json
// kickoffs/mock-2018-r2026.json
{
  "schema": 1,
  "id": "mock-2018-r2026",
  "label": "POWER UP field · 2026 robot rules",
  "gameYear": 2018,
  "game": "powerup-2018",
  "robotRulesYear": 2026,
  "robotRules": "robot-2026",
  "updates": ["robot-2027"],
  "dropGameRules": ["G05", "R03", "R04", "R05"],
  "overrides": []
}
```

```json
// rules/robot-2026.json (numbers from 2026 manual TU22 + inspection checklist)
{
  "schema": 1, "id": "robot-2026", "year": 2026,
  "rules": [
    {"id": "R103", "kind": "weight", "maxLb": 115.0, "src": "2026 manual R103"},
    {"id": "R104", "kind": "start", "perimeterMaxIn": 110, "heightMaxIn": 30, "src": "R104; inspection checklist"},
    {"id": "R105", "kind": "extension", "maxIn": 12, "src": "R105"},
    {"id": "R106", "kind": "oneSide", "src": "R106"},
    {"id": "R107", "kind": "height", "maxIn": 30.0, "exceptions": [], "src": "R107; G413 A-D damage/momentary only"}
  ]
}
```

```json
// rules/robot-2027.json (delta on robot-2026; FIRST previews 2026-08-31 and 2026-10-22)
{
  "schema": 1, "id": "robot-2027", "year": 2027, "extends": "robot-2026",
  "deltas": [
    {"id": "motors-18", "kind": "motorCount", "max": 18, "status": "preview", "src": "2027 preview part 1"},
    {"id": "no-heat-cool", "kind": "note", "status": "preview", "src": "part 1 (FTC E510 equivalent)"},
    {"id": "usb-100wh", "kind": "note", "status": "preview", "src": "part 1"},
    {"id": "canivore-2027", "kind": "note", "status": "preview", "src": "part 1 (R717 equivalent kept for 2027 only)"},
    {"id": "drop-talon-victorsp", "kind": "legalDevice", "status": "preview", "src": "part 1"},
    {"id": "drop-bag-minicim", "kind": "legalDevice", "status": "preview", "src": "part 1"},
    {"id": "no-relays", "kind": "legalDevice", "status": "preview", "src": "part 2"},
    {"id": "servo-power", "kind": "legalDevice", "status": "preview", "src": "part 2"},
    {"id": "r623-cots-connectors", "kind": "note", "status": "preview", "src": "part 2"},
    {"id": "new-devices", "kind": "legalDevice", "status": "preview", "src": "part 2 (Koors40 CAN, Littelfuse 120 A, Thrifty PowerHub, SPARK Lite, VH-109 V2, ...)"}
  ]
}
```

Effective rule row (what the UI and checks consume):
`{id, kind, value, layer: "game"|"robot"|"update"|"mock", year, status, src, replaced?: "G05"}`. The existing `SideViewGameProfile` is
produced from it (`r107MaxM`, `r105PastFrameM`, `r104StartHeightM`, `rules.*`, `overlayId`, `vision`), so every page keeps working.

Public 2027 state (web search, 2026-11-09): **2 preview blogs, ~10 rule bullets plus a new-device list**, none touching extension or
height. No 2027 Team Updates exist yet (Team Update 00 comes with the kickoff manual). Sources:
[part 1](https://www.firstinspires.org/community-blog/2026-event-robot-rule-preview-for-2027-season-part-1),
[part 2](https://www.firstinspires.org/community-blog/2026-event-robot-rule-preview-for-2027-season-part-2).

Robot-rule diff the kickoff page should show:

| Rule | 2018 | 2026 | 2027 preview |
| --- | --- | --- | --- |
| Weight | 120 lb (R05) | 115 lb (R103) | unchanged so far |
| Start size | 33 x 28 x 55 in volume (R03) | perimeter <= 110 in, height <= 30 in (R104) | unchanged so far |
| Extension | 16 in, Platform-zone endgame exempt (R04/G05) | 12 in (R105), one side (R106) | unchanged so far |
| In-match height | none | 30 in (R107) | unchanged so far |
| Motors | no count cap | no count cap | **18 max** |

## 7. Overlay checklist (`powerup-2018.json` vs 2018 manual text)

Every number currently in the overlay was checked against the manual text and matches (fence 12 ft 9.5 x 4 ft 8 x 18.75 in; switch plates
3 x 4 ft at 9 in level, owned 3-6 in, neutral 6-15 in; scale level 5 ft +/- 1 in, owned 48-56 in, opponent 64-72 in; 3.5 in near walls,
15 in centre wall; exchange 77.75 in wall, 16.25 x 21 in opening; return and portal 14 in square at 20 in; cube 13 x 13 x 11 in).

Modelled (OK): switch fence, switch plate (level), switch owned edge, scale owned / level / opponent plates, scale near lip, exchange wall,
exchange opening, exchange return, portal opening, power cube (two scenes).

Wrong or misleading:

| Item | Problem | Fix |
| --- | --- | --- |
| `sideViewGame.ts` powerup-2018 `vision: 'none'`, `retro.py` `"2018": "none"` | Manual 3.9: retro tape on switch fence | `retro` for the real profile (D7); the mock game and aprilsim season use `tag` (section 4) |
| Top-level `note` "PROPOSED (audit 2026-10-29)" | Status stale; reads as unapproved | Drop "PROPOSED" or mark accepted |
| `switch-plate` `approx: false` while `src` says "drawing estimate" for the 4 in inset | Inconsistent flag (the inset agrees with the manual's 1.5 in gap + fence wall) | Cite the 1.5 in gap; keep `approx: false` |
| `scale-lip` drawn only at the level state | Lip moves with the plate | One lip per state or label "at level" (already says so; low priority) |
| `exchange-*` / `portal-open` outlines use a 0.03 m synthetic depth with `approx: false` | Depth is not a manual number | `approx: true` on depth, or note it |

Missing (needed for the MVP board marked *):

| Element | Manual numbers | Notes |
| --- | --- | --- |
| Platform + ramp * | top 3.5 in, 8 ft 8 x 3 ft 5.25 in, ramp 13.75 in run at 15.35 deg | New `platform` scene; park target |
| Rung * | top 84 in, 1.25 in Sch 40 pipe, 13 in long, 8.25 in from tower face | Climb target; the R107 headline |
| Switch neutral / far-plate state * | 6-15 in | Only the owned edge is drawn |
| Exchange ramp * | 1.75 in tall x 6.5 in deep | Matters for floor-level ejectors |
| Tower / outriggers | tower 17 in wide, 2 in proud of outriggers | Scale scene structure |
| Null territory | 7 ft 11.25 in (see manual 2.x) | Top-down (aprilsim) |
| Power cube zone + pyramid | 3 ft 9 x 3 ft 6 in; pyramid count to verify (10) | Top-down |
| Cubes along switch fence | count to verify (6 per switch) | Top-down |
| Auto line, exchange zone (4 x 3 ft), portal zone (4 ft x 12 ft 11 in) | manual 3.2 | Top-down |
| Vault (human only) | 3 columns 13.5 x 39.25 in, bottom 15.5 in | Display only |
| Vision tape (real 2018 profile) | two 16 in strips, 4 in gap, centre 51 7/8 in from switch centre (manual 3.9) | Retro pipeline later; the mock uses the tag retrofit (section 4) |
| Plate colour assignment (game data) | randomised at AUTO start | Game state, not geometry |
| Scale / switch tilt dynamics, ownership timing | weight-driven | Out of scope |

Also unmodelled in the 2018 profile (and moot under Option L): the 2018 start volume 33 x 28 in footprint and the G05 Platform-zone endgame
exemption.

## 8. Mockup brief for Sonnet (HTML wireframe only)

Deliverable: one self-contained static file, `docs/mockups/mock-kickoff-2018-wireframe-20261109.html` in this store. Grey-box wireframe,
no build, no framework, no data fetching (inline sample data from sections 0, 4 and 6), RaidZero dark theme colours optional. Not production
code; do not touch `RaidZero-Simulation`. Use a grey video placeholder box labelled "FIRST POWER UP game animation (YouTube embed)"
instead of a real embed.

Put a **defaults strip** at the very top: the D1-D13 table from section 1 as compact chips (default shown, alternative on hover), with
one "Confirm all defaults" button and a note box. Then, in order, one scrollable page with an "Allan: approve / change" note box after each
panel:

1. **Top bar as on `:8050`**: existing route chips plus a "Kickoff" chip (D3); Game pill "POWER UP field · 2026 robot rules · 2027 preview";
   a small "TAS only" badge (D12).
2. **Cold open + welcome** (section 3 blocks 1-2): video placeholder, the welcome copy draft verbatim, layer chips (Field 2018, Robot rules
   2026, Updates 2027 preview) with source-link icons, and the Option L / M toggle (D1).
3. **Field tour**: five element cards with 2018 numbers and the red/amber/green "under 2026 rules" strip.
4. **Reachability board** (main panel): rows = Exchange opening, Return/Portal, Platform, Switch, Scale low/level/high, Rung; columns =
   target height, verdict chip (Reachable / Marginal / Launch only / Impossible), deciding rule (R107, R105), "Open in Elevator / Orbit /
   Double arm". One row expanded with the side-view sketch (cap line at 30 in, fence at 18.75 in, cube). A D2 toggle flips the Switch row.
5. **Rule diff + Team Update feed**: the section 6 diff (2018 / 2026 / 2027 preview) with `preview` badges and "replaced G05" on
   extension; below it the empty "Mock TU 00" feed with "+ add override" showing how a mock row looks.
6. **Vision card** (section 4): top-down 54 x 27 ft field sketch with the 20 tag dots coloured by group (switch, exchange/portal, scale
   tower, scale plates), a side inset of one scale plate with the hanging tag panel, a θ slider (-7.66 to +7.66 deg) that moves the inset and
   shows edge height, tag z and state (owned / level / opponent), and an "Open AprilTag route (season 2018)" link.
7. **Mechanism page banner** (small inset): "Kickoff: POWER UP · 2026 rules · target Switch (reachable under R107, cube not counted)".

## 9. Next steps (after Allan confirms defaults and approves the wireframe)

1. Overlay fixes and missing MVP elements (section 7 starred); vision flags (D7, mock `tag`).
2. `rules/*.json`, `kickoffs/mock-2018-r2026.json`, `kickoffCompose.ts` + tests, parity test extension.
3. aprilsim: field-drawing pass for the TBD tag poses, `2018-powerup-tas-retrofit.json`, `SeasonSpec("2018")`, `with_scale_tilt`, scale
   readout, tests.
4. `#/kickoff` route and Game entry.
5. Later: scale time schedule, exchange/switch cycle drives, retro-tape pipeline for the real 2018 profile.
