# Holistic Physiotherapy & Wellness (HPW): handouts and images

## Exercise programs (standing rules)
- **Use real people in every exercise image** for this program and any future exercise program. Don't use line drawings or stick figures.
  - Source: realistic AI photos from the connected Canva account (`generate-image`). Use one landscape 4:3 image per exercise, with two side-by-side panels of the same person (start | finish).
  - Show a mix of people across exercises (age, gender, ethnicity, body type), in a bright clinic setting. Clothing: dark teal t-shirt (brand colour) and black bottoms.
  - Check every image for correct form (joint angles, rib position, grip) before using it. Regenerate any that are wrong.
  - To download full-size images, the environment's network policy must allow `media.canva.com` and `export-download.canva.com`.
- Before building, ask clarifying questions using question cards (client level, format, equipment, schedule).
- Use Canadian spelling and plain language, and include a safety or red-flags section.
- Cite research via PubMed with DOIs.

## Brand kit (HPW Brand Kit, Oct 2025, Final v4)
| Role | Name | HEX |
|---|---|---|
| Headings, bars, accents | Dark Teal (Primary) | #0B4C5F |
| Highlights, icons, dividers | Medium Teal | #1C7B8D |
| Backgrounds, visuals | Light Teal | #7FC4C9 |
| Strong accents (website) | Primary Gold | #C9A56A |
| Calm backgrounds | Soft Gold | #DCC6A1 |
| Gentle accents | Soft Blush Pink | #E8BFC3 |
| Body text | Charcoal Grey | #3C3C3C |
| Print black | Rich Charcoal Black | #1C1C1C |
| Backgrounds | Soft White | #FAFAFA |
| Dividers | Light Grey | #E5E7E9 |
| Warm neutral (print) | Stone Taupe | #C8BFB3 |

- Fonts: Montserrat Bold/Semi-Bold for headings; Montserrat Regular/Light for body text; Raleway Medium Italic for accents and quotes; Brittney (the logo script) sparingly.
- Logo: the watercolour tree in a gold double circle, with "HOLISTIC" in a serif and "Physiotherapy & Wellness" in script. The mark is at `pull-up-program/source/assets/logo.png`. Rebuild the horizontal lockup with Cinzel + a script font (Great Vibes stands in for Brittney).
- Digital: teals + Primary Gold. Print: Rich Charcoal Black on Soft White for contrast.

## Existing work
- `pull-up-program/`: 12-week "Road to Your First Pull-Up" handout (PDF, images, and build sources in `source/`).
  - Photos live in `source/photos/<key>.jpg` (copies in `images/`). Canva media IDs are in `source/photos.json`.
  - To download Canva images at print quality: create a temporary design, add one 1456×1088 page per image, `insert_fill` each image full-page, then download the `thumbnail_urls` that `edit-design` returns (600 px wide, on export-download.canva.com). Cancel the transaction afterwards; nothing needs saving.
