import json,re,sys,glob
CH={"padkos":"Padkos","tv":"Cooking with TV","family":"Family Favourites","sweet":"Sweet Dreams","drinks":"Cocktails and Drinks"}
out=[];r=None;sec=None
for fn in sorted(glob.glob(sys.argv[1]+"/r[1-5].txt")):
  for line in open(fn,encoding="utf8"):
    line=line.rstrip("\n")
    if not line.strip(): continue
    k,_,v=line.partition(" ")
    if line.startswith("@ "):
      t,c,p=[x.strip() for x in line[2:].split("|")]
      slug=re.sub(r"[^a-z0-9]+","-",t.lower().replace("’","")).strip("-")
      r={"id":slug,"title":t,"section":c,"sectionName":CH[c],"page":int(p),"serves":"","time":"","headnote":"","groups":[],"tips":[],"caption":"","source":"The Optimist Cookbook"};out.append(r);sec=None
    elif line.startswith("s:"): r["serves"]=line[2:].strip()
    elif line.startswith("t:"): r["time"]=line[2:].strip()
    elif line.startswith("c:"): r["caption"]=line[2:].strip()
    elif k==">": r["headnote"]=v
    elif k=="!": r["tips"].append(v)
    else:
      if k=="#": sec={"heading":v,"ingredients":[],"steps":[]};r["groups"].append(sec);continue
      if sec is None: sec={"heading":"","ingredients":[],"steps":[]};r["groups"].append(sec)
      if k=="-": sec["ingredients"].append(v)
      elif k==".": sec["steps"].append(v)
      else: raise SystemExit("bad line: "+line)
json.dump(out,open(sys.argv[1]+"/recipes.json","w"),ensure_ascii=False,indent=1)
print(len(out), sum(len(g["ingredients"]) for r in out for g in r["groups"]),"ingredients", sum(len(g["steps"]) for r in out for g in r["groups"]),"steps")
print([r["title"] for r in out if not any(g["ingredients"] for g in r["groups"]) or not any(g["steps"] for g in r["groups"])])
