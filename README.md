# The Optimist Cookbook App

The family recipe app for *The Optimist Cookbook*. It is hosted as a private claude.ai artifact:
https://claude.ai/artifact/3otud1RsnLVJ4jgmbYRp2d

## What it does
- Lists all 362 recipes: the 49 from The Optimist Cookbook (Vol. 1, with photos) and 313 from the Vol. 2 draft, by chapter.
- Vol. 2 recipes show a "Vol. 2" tag, their source, any Afrikaans name, and a red "Check before printing" note where the source was incomplete. They cannot be deleted from the app.
- Browse by course (Starters, Soups & Small Plates; Mains; Braai & Potjie; Breads & Bakes; Sweet Dreams; Sides, Sauces & Basics; Cocktails and Drinks), and filter by story tag: Family, Food Truck & Padkos, TV & Chefs, Vol. 1, or Added in the app.
- Search by recipe name or ingredient.
- **Add recipe**: photograph a recipe (one or more photos) or upload a social media screenshot. Claude reads it, lays it out in the cookbook format (title, introduction, serves | total time, ingredients and method per part, tips) and files it in the section you choose. You check and edit it before it is saved.
- Edit any recipe; delete recipes the family added (book recipes cannot be deleted from the app).
- Shared live between everyone the artifact is shared with.

## How it is built
- `src/app.template.html` - the whole app (HTML, CSS, vanilla JS). Uses the artifact runtime capabilities `db` (shared recipe database), `assets` (photos), `sample` with images (Claude reads the photos) and `user` (who added a recipe).
- `tools/build.py` - inlines the Optimist font and cover texture, writing `dist/the-optimist-cookbook-app.html`, which is the file published to the artifact.
- `data/transcriptions/r1-r5.txt` - the book recipes, transcribed by hand from the PDF (one file per chapter). `tools/transcriptions_to_json.py` turns them into `data/recipes.json`.
- `data/photo-asset-ids.txt` - which artifact asset holds each book photo.
- `data/vol2/vol2.json` - the recipe data from the Vol. 2 draft artifact. `tools/vol2_to_app.py` converts it to `data/vol2/app-recipes.json` (skipping the 49 Vol. 1 recipes already in the app), which was written to the database.
- `tools/reorganise_courses.py` - moved recipes from the Vol. 1 story chapters (Padkos, Cooking with TV, Family Favourites) to courses with `stories` tags. `data/reorg/course-assignments.md` lists the 71 recipes that were given a course.
- `tools/vol2_apply_checks.py` - the check-note fixes approved on 23 Oct 2026 (Certain or Likely only). Resolved notes are kept in `resolvedChecks` with their confidence rating.

Fonts: Optimist (titles, custom font) and Aleo (body, Google Fonts - the same body font the printed book uses).

## Data model (`recipes/<id>`)
`title, altTitle, section (the course), stories[] (family|padkos|tv), page (Vol. 1 sort order only, not shown), serves, time, headnote, groups[{heading, ingredients[], steps[]}], tips[], checks[], resolvedChecks[], caption, credit, source, book ("The Optimist Cookbook" | "The Optimist Cookbook Vol. 2" | "Added"), origin (book|vol2|photo|social), photo (asset id), scans (asset ids), addedBy (account id), addedByName (the name the person typed), addedAt`

Extra sections created in the app are stored in `meta/sections`.
