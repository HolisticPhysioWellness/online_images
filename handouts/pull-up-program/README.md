# Road to Your First Pull-Up

A 12-week client handout from Holistic Physiotherapy & Wellness. It's for clients who can hang from a bar but can't do a pull-up yet. The program runs 2 sessions a week and uses bodyweight, a pull-up bar and resistance bands.

- `road-to-your-first-pull-up-2026-09.pdf`: the printable 12-page handout (Letter size).
- `images/`: the real-person start/finish photo for each exercise (AI-generated in Canva), for use on the website or in JaneApp.
- `source/`: the files that build the PDF (`build.py`, `handout.css`, the photos, the logo and the fonts).

## Program outline
| | |
|---|---|
| Daily | Wall angels: breathe in as the arms rise, out as they lower, with rib-flare cues |
| Warm-up | 90/90 breathing, dead bug, cat–camel, scapular push-ups, band pull-aparts, wall angels |
| Phase 1 (wk 1–4) | Scapular pull-ups + active hang, inverted row, band lat pull-down, prone Y raise, hollow body (tucked) |
| Phase 2 (wk 5–8) | Active hang primer, negative pull-ups, flexed-arm hang, band-assisted pull-ups, inverted row, hollow body |
| Phase 3 (wk 9–12) | Primer + easy band set, pull-up attempts, slow negatives, band-assisted pull-ups, inverted row, flexed-arm hang, hollow body (full) |

Each phase ends with a checklist. The client moves on once they pass it, and Phase 3 ends with a test-day checklist. The exercise order follows the priority-first and multi-joint-first research cited in the handout.

## Rebuilding
Run `source/build.sh`. It needs Python 3 and Node with Playwright/Chromium. To swap a photo, save it as `source/photos/<key>.jpg`; the Canva media IDs are in `source/photos.json`.
