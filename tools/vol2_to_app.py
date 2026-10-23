"""Convert the Vol. 2 draft data (data/vol2/vol2.json, the DATA object from the Vol. 2 draft artifact)
into app recipe documents (data/vol2/app-recipes.json).

Recipes flagged vol1 are skipped: they are already in the app as book recipes.
Ingredient and method groups are merged by heading where they match; otherwise the
ingredient parts come first and the method parts follow, so nothing is lost or reworded.
"""
import json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = json.loads((root / "data/vol2/vol2.json").read_text(encoding="utf8"))
VOL2 = "The Optimist Cookbook Vol. 2"


def groups(r):
    ing = [{"heading": g["group"], "items": g["items"]} for g in r["ingredients"]]
    met = [{"heading": g["group"], "items": g["steps"]} for g in r["method"]]
    if [g["heading"] for g in ing] == [g["heading"] for g in met]:
        return [{"heading": a["heading"], "ingredients": a["items"], "steps": b["items"]} for a, b in zip(ing, met)]
    out = [{"heading": g["heading"], "ingredients": g["items"], "steps": []} for g in ing]
    if len(met) == 1 and not met[0]["heading"]:
        if len(out) == 1 and not out[0]["heading"]:
            out[0]["steps"] = met[0]["items"]
        else:
            out.append({"heading": "Method", "ingredients": [], "steps": met[0]["items"]})
        return out
    by = {g["heading"].lower(): g for g in out}
    for g in met:
        hit = by.get(g["heading"].lower())
        if hit is not None and not hit["steps"]:
            hit["steps"] = g["items"]
        else:
            out.append({"heading": g["heading"] or "Method", "ingredients": [], "steps": g["items"]})
    return out


docs = []
for r in src["recipes"]:
    if r.get("vol1"):
        continue
    d = {
        "title": r["title"],
        "section": r["ch"],
        "page": None,
        "serves": r.get("serves", ""),
        "time": r.get("time", ""),
        "headnote": r.get("intro", ""),
        "groups": groups(r),
        "tips": r.get("tips", []),
        "caption": "",
        "credit": r.get("credit", ""),
        "source": r.get("src", ""),
        "book": VOL2,
        "origin": "vol2",
        "photo": None,
        "scans": [],
        "addedBy": None,
        "addedAt": 0,
    }
    if r.get("af"):
        d["altTitle"] = r["af"]
    if r.get("checks"):
        d["checks"] = r["checks"]
    docs.append({"id": r["id"], "data": d})

(root / "data/vol2/app-recipes.json").write_text(json.dumps(docs, ensure_ascii=False, indent=1), encoding="utf8")
print(len(docs), "recipes written to data/vol2/app-recipes.json")
