# Road to Your First Pull-Up

A 12-week client handout from Holistic Physiotherapy & Wellness. It's for clients who can hang from a bar but can't do a pull-up yet. The program runs 2 sessions a week and uses bodyweight, a pull-up bar and resistance bands.

- `Road-to-Your-First-Pull-Up.pdf`: the printable 11-page handout (Letter size).
- `images/`: the real-person start/finish photo for each exercise (AI-generated in Canva), for use on the website or in JaneApp.
- `source/`: the code that generates the drawings and the PDF.

## Program outline
| | |
|---|---|
| Daily | Wall angels, with rib-flare cues and a correct vs. incorrect side view |
| Warm-up | 90/90 breathing, cat–camel, band pull-aparts, scapular push-ups, dead bug, wall angels |
| Phase 1 (wk 1–4) | Scapular pull-ups + active hang, band lat pull-down, prone Y raise, inverted table row, hollow body (tucked) |
| Phase 2 (wk 5–8) | Band-assisted pull-up, flexed-arm hang, negatives, rows, hollow body |
| Phase 3 (wk 9–12) | Pull-up attempts, paused slow negatives, light-band pull-ups, hollow body (full), rows |

Each phase ends with a checklist. The client moves to the next phase once they pass it.

## Rebranding and rebuilding
1. Put the brand kit colours and fonts into the `BRAND KIT` block at the top of `source/handout.css`. Change the figure colours at the top of `source/fig.py`.
2. To use the real logo, replace the round "HP" placeholder in `header()` in `source/build.py`, and do the same on the cover page.
3. Run `source/build.sh`. It needs Python 3 and Node with Playwright/Chromium. It regenerates the drawings, PNGs and PDF.
