"""Build Envato image prompts for the Vol. 2 recipes without photos (data/vol2/photo-prompts.json).

Style matches the Vol. 1 book photos: dark, moody, warm side light, wooden table, close-up, 9:16 portrait.
"""
import json, pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
docs = json.loads((root / "data/vol2/app-recipes.json").read_text(encoding="utf8"))
SKIP = {"egg-boiling-times", "quick-pickling-brine", "crispy-batter-mix"}  # reference notes, not dishes
UNIT = r"(?:\d[\d/.,½¼¾⅓⅔ ]*|a |an |one |two |three |few |handful |pinch |splash |dash |generous |good |large |small |medium |big |extra[- ]large )*"
MEAS = r"(?:kg|g|ml|l|litres?|liters?|cups?|cup|tbsp|tsp|tablespoons?|teaspoons?|cloves?|tins?|cans?|packets?|bunch(?:es)?|sticks?|sprigs?|x|pieces?|slices?|rolls?|bars?|sheets?|heads?|stalks?|of)\b\.?\s*"
FOOD = "Professional cookbook food photograph of {t}{w}, plated on rustic crockery on a dark wooden table. Moody dark background, warm directional side light, shallow depth of field, close-up, realistic, appetising, no text, no people."
DRINK = "Professional cookbook drinks photograph of {t}{w}, in a suitable glass with garnish on a dark wooden bar. Moody dark background, warm directional side light, shallow depth of field, close-up, realistic, no text, no people, no labels."


def clean(s):
    s = s.split(",")[0].split("(")[0].strip()
    s = re.sub(r"^" + UNIT, "", s, flags=re.I)
    s = re.sub(r"^" + MEAS, "", s, flags=re.I)
    s = re.sub(r"^" + MEAS, "", s, flags=re.I)
    return s.strip(" .-").lower()


out = []
for d in docs:
    r = d["data"]
    if d["id"] in SKIP:
        continue
    ings = [clean(i) for g in r["groups"] for i in g["ingredients"]]
    ings = [i for i in ings if 2 < len(i) < 40 and not re.search(r"\d|½|¼|¾|salt|pepper|water|oil|to serve|ice\b|optional|garnish", i)]
    seen = []
    for i in ings:
        if i not in seen:
            seen.append(i)
    w = " made with " + ", ".join(seen[:4]) if seen else ""
    t = re.sub(r"\s*\((?:notes|batched|party batch|vegan|masterclass version|big batch)\)", "", r["title"], flags=re.I)
    out.append({"id": d["id"], "title": r["title"], "prompt": (DRINK if r["section"] == "drinks" else FOOD).format(t=t, w=w)})
(root / "data/vol2/photo-prompts.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf8")
print(len(out), "prompts")
for o in out[:3] + out[150:152] + out[-2:]:
    print("-", o["prompt"][:230])
