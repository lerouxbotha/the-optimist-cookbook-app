# The Optimist Cookbook App

The family recipe app for *The Optimist Cookbook*. It is hosted as a private claude.ai artifact:
https://claude.ai/artifact/3otud1RsnLVJ4jgmbYRp2d

## What it does
- Lists all 49 recipes from The Optimist Cookbook, by chapter, with their photos.
- Search by recipe name or ingredient.
- **Add recipe**: photograph a recipe (one or more photos) or upload a social media screenshot. Claude reads it, lays it out in the cookbook format (title, introduction, serves | total time, ingredients and method per part, tips) and files it in the section you choose. You check and edit it before it is saved.
- Edit any recipe; delete recipes the family added (book recipes cannot be deleted from the app).
- Shared live between everyone the artifact is shared with.

## How it is built
- `src/app.template.html` - the whole app (HTML, CSS, vanilla JS). Uses the artifact runtime capabilities `db` (shared recipe database), `assets` (photos), `sample` with images (Claude reads the photos) and `user` (who added a recipe).
- `tools/build.py` - inlines the Optimist font and cover texture, writing `dist/the-optimist-cookbook-app.html`, which is the file published to the artifact.
- `data/transcriptions/r1-r5.txt` - the book recipes, transcribed by hand from the PDF (one file per chapter). `tools/transcriptions_to_json.py` turns them into `data/recipes.json`.
- `data/photo-asset-ids.txt` - which artifact asset holds each book photo.

Fonts: Optimist (titles, custom font) and Aleo (body, Google Fonts - the same body font the printed book uses).

## Data model (`recipes/<id>`)
`title, section, page, serves, time, headnote, groups[{heading, ingredients[], steps[]}], tips[], caption, credit, book, origin (book|photo|social), photo (asset id), scans (asset ids), addedBy, addedAt`

Extra sections created in the app are stored in `meta/sections`.
