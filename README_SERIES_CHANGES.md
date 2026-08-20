# Series (Brand) cleanup — 3 curated Series only

## What changed

The "Series" dropdown in the Add-Item wizard now shows exactly **3** options
instead of the old cluttered list:

1. **CutFlow Standard** — only the 2 Track (`SY02`) and 3 Track (`SY03`)
   sliding systems, with their topologies. (SY03 also gets 2 new
   mosquito-mesh topology options — `2S1M` and `1S1F1M` — inspired by the
   mosquito shutter design options in the reference 26mm sliding window
   manual.)
2. **Generic** — every other existing System (SY01 casement, and
   SY04–SY08 / AL01 / UP01 if they exist in your DB) is bucketed here.
3. **Jindal-Domal** — a brand-new 2 Track / 3 Track sliding series
   (`JD01` / `JD02`), fully wired with its own profiles, cut formulas,
   hardware rules and topologies, so "Preview Bar Optimization" works for
   it out of the box, same as CutFlow Standard. Panel configurations are
   modelled on generic industry-standard 2T2P / 3T3P sliding assemblies
   (topology names/shapes only — no proprietary die numbers, dimensions,
   or cutting-list data were copied from any manufacturer's manual).

Any other Brand row that already exists in your database (e.g. the old
empty placeholder brands — Rehau / VEKA / Schuco / Aluplast / Fenesta —
that had zero systems attached and were the "empty" options you were
seeing) is **deactivated**, not deleted, so it silently disappears from
the Series dropdown without touching any foreign keys.

## Files in this zip

```
catalog/
  models.py                                  (modified: + 'mesh' panel type)
  migrations/
    0011_reorganize_series.py                (new: the actual data migration)
  management/commands/
    seed_data.py                             (modified: brand routing fix)
    seed_remaining_systems.py                (modified: brand routing fix)
    seed_system_profiles.py                  (modified: brand routing fix)
core/
  management/commands/
    seed_data.py                             (modified: brand routing fix)
templates/projects/
  project_detail.html                        (modified: renders 'mesh' panels
                                               as a cross-hatch pattern)
```

Drop these into your project (overwriting the existing files at the same
paths) and run:

```bash
python manage.py migrate
```

That's it — `0011_reorganize_series.py` does all the work automatically:
creates/activates the 3 target brands, reassigns every existing System to
the correct one, deactivates stray brands, and seeds the full Jindal-Domal
catalog (profiles, formulas, hardware, topologies).

## Why the management commands were also touched

`catalog/management/commands/{seed_data,seed_remaining_systems,
seed_system_profiles}.py` and `core/management/commands/seed_data.py` are
the original (pre-migration) seed scripts. They're not required for normal
operation any more since migration `0003` and `0010` already seed the core
data — but if you (or a teammate) ever re-run one of them against a fresh
or partially-empty DB, the **old** versions would have recreated the empty
Rehau/VEKA/Schuco/Aluplast/Fenesta brands and dumped SY02/SY03 back under
the wrong bucket. I updated them so they're consistent with the new
3-Series scheme and safe to re-run at any time.

## Verified end-to-end

I tested this locally against a scratch SQLite DB before packaging:

- Fresh `migrate` from zero → exactly 3 active Brands, correct System →
  Brand assignments, correct topology counts.
- Re-running the legacy `seed_remaining_systems` command afterwards still
  routes SY04–SY08 into **Generic** (not CutFlow Standard).
- `/catalog/api/systems/?brand=<Jindal-Domal id>` and
  `/catalog/api/topologies/?system=<JD02 id>` both return the expected
  JSON.
- Created a real `MeasurementItem` on `JD02` / topology `2S1M` and hit
  `/projects/measurements/<pk>/optimize-preview/` — it returned a full,
  correct bar-optimization result (9 bars packed, 67.3% utilisation, 30 cut
  pieces) with zero errors.
- Ran the same preview check against `SY01`, `SY02`, and `SY03` (including
  the new `2S1M` topology on SY03) to confirm no regressions.
- `python manage.py check` and `makemigrations --check --dry-run` both come
  back clean (no missing migration state from the `models.py` change).

## One thing worth knowing

Since Jindal-Domal is a well-known real-world series name, I want to be
upfront: I did **not** have access to Jindal's actual proprietary profile
dimensions, die numbers, or cutting-list data, and didn't fabricate any as
if they were real Jindal specs. The `JD01`/`JD02` catalog data I generated
(profile weights, costs, formulas, hardware) is realistic placeholder data
in the same shape as your existing CutFlow Standard data — treat it as a
starting scaffold to overwrite with your real supplier spec sheet via
Django admin (`/admin/catalog/profile/`, `/admin/catalog/profileformula/`,
`/admin/catalog/systemhardwarerule/`) whenever you have it, rather than as
verified real-world numbers.
