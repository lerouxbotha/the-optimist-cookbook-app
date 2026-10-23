"""Apply the 'check before printing' fixes that Leroux approved on 23 Oct 2026
(only those rated Certain or Likely). Every other note stays flagged in the app.

Resolved notes move from `checks` (shown in red) to `resolvedChecks` (kept for the record,
not shown), each with the confidence rating and what was done.
Writes data/vol2/app-recipes.json in place and data/vol2/check-updates/<id>.json
(the changed fields only, for the database update).
"""
import json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
path = root / "data/vol2/app-recipes.json"
docs = json.loads(path.read_text(encoding="utf8"))
D = {d["id"]: d["data"] for d in docs}


def step(rid, old, new):
    for g in D[rid]["groups"]:
        for k in ("steps", "ingredients"):
            for i, s in enumerate(g[k]):
                if old in s:
                    g[k][i] = s.replace(old, new)
                    return
    raise SystemExit(f"not found in {rid}: {old}")


def tip(rid, text):
    D[rid]["tips"] = D[rid].get("tips", []) + [text]


# (id, confidence, what was done, edit function or None, replacement check text or None)
FIXES = [
    ("condensed-milk-fudge", "Likely", "½ cup water kept (the usual amount).", None, None),
    ("beef-bourguignon", "Likely", "Celery already goes in with the carrots; beurre manié set at about 1 tbsp each.",
     lambda r: step(r, "Mix a little soft butter and flour to a paste", "Mix about 1 tbsp soft butter and 1 tbsp flour to a paste"), None),
    ("masterchef-chilli-con-carne", "Likely", "Kidney beans go in with the stock.",
     lambda r: step(r, "Add the red pepper, tomatoes and stock (and the beans, see note)", "Add the red pepper, tomatoes, stock and kidney beans"), None),
    ("nougat-pound-cake", "Likely", "325 g butter, matching the Vanilla Pound Cake it is based on.",
     lambda r: step(r, "325 g butter (see note)", "325 g butter"), None),
    ("croque-monsieur-breakfast-casserole", "Likely", "Croissants set at 4 to 5.",
     lambda r: step(r, "A good handful day-old croissants", "4 to 5 day-old croissants (a good handful)"), None),
    ("wild-mushroom-tortellini", "Likely", "Serving suggestion added as a tip.",
     lambda r: tip(r, "Serve with brown butter and sage, or a little cream and Parmesan."), None),
    ("bertus-basson-s-steamed-pork-rice", "Certain", "Note is cooking advice, moved to a tip.",
     lambda r: tip(r, "4 parts water to 1 part rice is a lot for jasmine rice: watch for the water dropping below the rice rather than the clock."), None),
    ("bacon-pea-risotto-balls", "Likely", "Parmesan stirred in at the end.",
     lambda r: step(r, "the last 2 tbsp butter and the Parmesan (see note)", "the last 2 tbsp butter and the Parmesan"), None),
    ("massaman-beef-roast-with-coconut-coriander-sauce", "Certain", "Printed doneness figures are Fahrenheit; Celsius core temperatures added.",
     lambda r: step(r, "Roast to your liking using a meat thermometer.", "Roast to your liking using a meat thermometer (core temperature about 52°C rare, 60°C medium, 65°C medium-well)."), None),
    ("dashi-mushroom-broth-restaurant-version", "Likely", "40 g sugar, added with the soy.",
     lambda r: step(r, "Bring the water, soy, ponzu, mirin and salt to the boil.", "Bring the water, soy, sugar, ponzu, mirin and salt to the boil."), None),
    ("peanut-butter-peri-peri-prawns", "Likely", "Garlic goes in with the butter.",
     lambda r: step(r, "Melt the butter in an extra-large pan, sauté the prawns", "Melt the butter in an extra-large pan, sauté the garlic briefly, then the prawns"), None),
    ("cheese-corn-bread", "Likely", "Creamed corn goes in with the wet ingredients (already in the method).", None,
     ["The spring onion quantity isn't shown in the source."]),
    ("one-pot-creamy-cauliflower-soup", "Likely", "Leeks cooked with the onion.",
     lambda r: step(r, "cook the onion (and leeks)", "cook the onion and leeks"), None),
    ("air-fryer-garlic-butter-flatbreads", "Likely", "Air-fry time set at 4 to 6 minutes a side.",
     lambda r: step(r, "Air-fry in batches until puffed and golden on both sides.", "Air-fry in batches, 4 to 6 minutes a side, until puffed and golden."), None),
    ("fried-chicken-kit-brine-seasoned-flour-chipotle-mayo-dill-pickles", "Likely", "Standard brining time and frying temperature added.",
     lambda r: (step(r, "brine the chicken in the fridge.", "brine the chicken in the fridge for at least 4 hours or overnight."),
                step(r, "dredge the drained chicken before frying.", "dredge the drained chicken and deep-fry at 170 to 175°C until golden and cooked through (75°C at the bone).")), None),
    ("egg-boiling-times", "Likely", "Timing from boiling water kept.", None, None),
    ("the-bianco-charrara-1", "Likely", "Shake-and-strain method kept.", None, None),
    ("kick-ass-bread-with-bertus", "Likely", "Water with the flour and a 10 g yeast sachet kept.", None, None),
    ("bertus-s-chocolate-fondant", "Likely", "Greased moulds and the yield kept.", None, None),
    ("apple-pistachio-tart-with-hot-milk-syrup", "Likely", "385 g tin of pie apples kept.", None, None),
    ("masterchef-koeksisters", "Likely", "Last step completed as written.", None, None),
    ("milk-tart-with-shattered-caramel", "Likely", "Standard caramel finish kept.", None, None),
    ("fresh-egg-pasta-everyday-special", "Certain", "Standard resting and rolling steps kept.", None, None),
    ("matt-manning-s-wild-boar-scotch-eggs", "Certain", "Flour-egg-crumb order kept.", None, None),
    ("sweet-lace-tuile", "Likely", "Standard lace tuile method kept.", None, None),
    ("stay-home-red-curry", "Likely", "Standard red curry method kept.", None, None),
    ("no-bake-raspberry-cheesecake", "Likely", "Final setting step kept.", None, None),
    ("chocolate-cake-with-chocolate-butter-icing", "Certain", "Raw-egg note moved to a tip.",
     lambda r: tip(r, "The icing uses raw eggs, so use very fresh eggs and skip it for anyone pregnant, elderly or very young."), None),
]

out = root / "data/vol2/check-updates"
out.mkdir(exist_ok=True)
for f in out.glob("*.json"):
    f.unlink()
for rid, conf, done, fn, keep in FIXES:
    r = D[rid]
    old = r.get("checks") or []
    assert old, rid
    if fn:
        fn(rid)
    r["resolvedChecks"] = [{"note": n, "confidence": conf, "resolution": done} for n in old]
    if keep:
        r["checks"] = keep
    else:
        r.pop("checks", None)
    upd = {"groups": r["groups"], "tips": r["tips"], "resolvedChecks": r["resolvedChecks"],
           "checks": r["checks"] if "checks" in r else {"__delete__": True}}
    (out / f"{rid}.json").write_text(json.dumps(upd, ensure_ascii=False), encoding="utf8")

path.write_text(json.dumps(docs, ensure_ascii=False, indent=1), encoding="utf8")
left = sum(1 for d in docs if d["data"].get("checks"))
print(len(FIXES), "recipes updated;", left, "still flagged")
