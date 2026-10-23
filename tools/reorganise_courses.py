"""Move the app from Vol. 1 chapters to courses plus story tags (23 Oct 2026).

Recipes in the story chapters (Padkos, Cooking with TV, Family Favourites) get a course;
every recipe gets `stories` from its old chapter and its source. Reads the database snapshot
directory given as argv[1] (recipes/<id>.json) and writes data/reorg/<id>.json updates
(section + stories) plus data/reorg/course-assignments.md for review.
"""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
snap = pathlib.Path(sys.argv[1])

COURSE = {
    # Padkos
    "bacon-pea-risotto-balls": "starters", "butter-chicken": "mains", "chocolate-truffle-vetkoek": "sweet",
    "churros-with-butterscotch-sauce": "sweet", "katkoppe-vetkoek-meatballs": "starters", "killer-croquettes": "starters",
    "lamb-kofta-boerewors-sosaties-notes": "braai", "poke-mon": "starters",
    "pork-ribs-with-turmeric-gnocchi-charred-corn-smoked-cream-cheese": "mains", "prawn-avo-mango-salad": "starters",
    "shake-your-brisket-gatsby": "mains", "slow-roast-lamb-pitas-with-tomato-blatjang": "mains", "taco-whiz": "mains",
    "the-clark-kent-calzone": "mains", "the-joker-hotdog": "mains", "the-spider-man-vetkoek": "mains",
    "the-vixen-burger": "mains", "west-coast-mussels": "mains", "white-chocolate-blondies": "sweet",
    # Cooking with TV
    "andrea-burgners-cilbir": "starters", "baby-squid-with-wakame-brioche-squid-ink-sauce": "starters",
    "bertus-basson-s-steamed-pork-rice": "mains", "bertus-bassons-caeser-salad": "starters",
    "bosduifklip-mussel-sosaties": "braai", "chef-henrys-cheesy-truffles": "starters", "chef-matt-s-carbonara": "mains",
    "chef-shanice-s-lamb-curry": "mains", "easy-milktart": "sweet", "gregg-hammonds-24-hour-herb-crusted-beef-fillet": "mains",
    "heirloom-tomato-and-whipped-feta-tart": "starters", "ilse-s-red-curry-of-beef-with-cucumber-relish": "mains",
    "la-mouette-salt-pepper-prawns-with-chorizo-popcorn": "starters", "masterchef-chilli-con-carne": "mains",
    "masterchef-koeksisters": "sweet", "moroccan-roast-carrot-and-avocado-salad": "starters",
    "peanut-butter-peri-peri-prawns": "mains", "stuffed-courgette-flowers-with-baby-marrow-veloute": "starters",
    "stuffed-saddle-of-lamb-with-sweet-potato-dauphinoise": "mains", "tomato-and-pancetta-braai-chicken-with-olives": "braai",
    "tuna-ceviche-with-guacamole-cream-pickled-papaya": "starters", "yorkshire-pudding": "basics",
    # Family Favourites
    "beef-lasagne": "mains", "biltong-soup": "starters", "broccoli-chicken-bake": "mains",
    "cannellini-beans-with-roast-tomatoes-basil": "basics", "chicken-lasagne": "mains", "chicken-rice-blatjang-chip-bake": "mains",
    "croque-monsieur-breakfast-casserole": "mains", "easy-focaccia": "breads", "eggs-benedict-on-rosti-with-smoked-trout": "mains",
    "eggs-benedict-pizza": "mains", "gazpacho": "starters", "h-s-sweet-tomato-soup": "starters",
    "ham-cheese-croissant-croque-monsieur": "mains", "handries-tamatiebredie": "mains", "homemade-labneh": "basics",
    "jhs-clear-chicken-soup-with-herb-dumplings": "starters", "kassie-s-savoury-tart": "starters",
    "lamb-boerewors-baked-in-batter-with-chilli-tomato-onion-sauce": "mains", "layered-pea-salad": "basics",
    "marikie-s-lasagne": "mains", "molshope-cheesy-potato-mounds": "basics", "mother-in-law-anitas-mac-n-cheese": "mains",
    "orzo-chicken-bake": "mains", "renette-s-broccoli-salad": "basics", "savoury-crepe-stack-with-spinach-feta-mushrooms": "mains",
    "seven-layer-salad": "basics", "sweet-potatoes-with-muscadel": "basics", "tatas-khuku": "mains",
    "whole-roasted-cauliflower-with-cheesy-b-chamel": "mains", "zannies-sweet-mustard": "basics",
}
NAMES = {"starters": "Starters, Soups & Small Plates", "mains": "Mains", "braai": "Braai & Potjie", "breads": "Breads & Bakes",
         "sweet": "Sweet Dreams", "basics": "Sides, Sauces & Basics", "drinks": "Cocktails and Drinks"}
OLD = {"padkos": "Padkos", "tv": "Cooking with TV", "family": "Family Favourites"}

out = root / "data/reorg"
for f in out.glob("*.json"):
    f.unlink()
rows, n = [], 0
for f in sorted((snap / "recipes").glob("*.json")):
    rid, r = f.stem, json.loads(f.read_text(encoding="utf8"))
    src = r.get("source", "")
    st = set(r.get("stories") or [])
    if r["section"] in OLD:
        st.add(r["section"])
    if re.search(r"Marikie|family|Auntie se Kookboek", src, re.I):
        st.add("family")
    if re.search(r"Padkos", src):
        st.add("padkos")
    if re.search(r"MasterChef|Plaaskombuis|ilsekook|Ilse Kook", src):
        st.add("tv")
    sec = r["section"]
    if sec in OLD:
        if rid not in COURSE:
            raise SystemExit("no course for " + rid)
        rows.append((OLD[sec], r["title"], NAMES[COURSE[rid]]))
        sec = COURSE[rid]
    stories = [s for s in ("family", "padkos", "tv") if s in st]
    if sec != r["section"] or stories != (r.get("stories") or []):
        (out / f"{rid}.json").write_text(json.dumps({"section": sec, "stories": stories}, ensure_ascii=False), encoding="utf8")
        n += 1
md = ["# Course assignments (23 Oct 2026)", "", "Recipes that were in a story chapter, with the course they now sit under. Story tags keep the old chapter.", "",
      "| Was in | Recipe | Now under |", "|---|---|---|"] + [f"| {a} | {b} | {c} |" for a, b, c in sorted(rows)]
(out / "course-assignments.md").write_text("\n".join(md) + "\n", encoding="utf8")
print(n, "recipes to update;", len(rows), "given a course")
