#!/usr/bin/env python3
# Prépare la grille "façon GitHub" des sauvegardes PBS pour le widget Homarr.
# Lit l'historique via le relais lecture seule et écrit /opt/pbs-relay/data/pbs-grid.json (servi par le relais en /pbs/grid).
import json, time, urllib.request, os
R = "http://127.0.0.1:8790"
get = lambda p: json.load(urllib.request.urlopen(R + p, timeout=30))["data"]
NAMES = {"100":"pfSense","101":"Docker-EXT","102":"Docker","104":"Jellyfin","105":"Nextcloud","106":"Bureau","202":"Site-asso","600":"VoIP","998":"Admin"}
COL = {"ok":"#2fb344","warn":"#228be6","err":"#e03131","none":"rgba(255,255,255,0.07)"}
day = lambda ts: int((ts + 3600) // 86400)          # jour à l'heure de Paris (hiver)
hist = get("/pbs/history"); groups = get("/pbs/buffalo")
today = day(time.time()); days = list(range(today - 29, today + 1))
rows = []
for g in sorted(groups, key=lambda g: int(g["backup-id"])):
    wid = "buffalo:%s/%s" % (g["backup-type"], g["backup-id"])
    rows.append((NAMES.get(g["backup-id"], g["backup-id"]), "%s %s" % (g["backup-type"], g["backup-id"]), True, lambda t, w=wid: t["worker_type"] == "backup" and t.get("worker_id") == w))
rows += [("Copie HDD", "chaque nuit", True, lambda t: t["worker_type"] == "syncjob"),
         ("Vérification", "dimanche", False, lambda t: t["worker_type"] == "verificationjob"),
         ("Nettoyage", "tri + GC", True, lambda t: t["worker_type"] in ("garbage_collection", "prunejob"))]
out = []
for label, sub, daily, match in rows:
    ts = [t for t in hist if match(t)]
    first = min((day(t["starttime"]) for t in ts), default=10**9)
    cells = []
    for d in days:
        L = [t for t in ts if day(t["starttime"]) == d]
        st = [t.get("status") or "en cours" for t in L]
        if not L: k = "err" if (daily and first <= d < today) else "none"
        elif any(s not in ("OK", "en cours") and not s.startswith("WARNINGS") for s in st): k = "err"
        elif any(s.startswith("WARNINGS") for s in st): k = "warn"
        else: k = "ok"
        quand = "aujourd'hui" if d == today else "il y a %d j" % (today - d)
        tip = quand + " : " + (", ".join(st) if L else ("rien ce jour-là" if k == "err" else "pas de tâche"))
        cells.append({"c": COL[k], "t": tip})
    out.append({"label": label, "sub": sub, "d": cells, "err": sum(1 for x in cells if x["c"] == COL["err"])})
os.makedirs("/opt/pbs-relay/data", exist_ok=True)
tmp = "/opt/pbs-relay/data/.pbs-grid.json"
stores = [{k: s[k] for k in ("store", "total", "used")} for s in get("/pbs/usage")]  # sans historique (limite Homarr)
json.dump({"data": {"rows": out, "stores": stores, "updated": int(time.time())}}, open(tmp, "w"), ensure_ascii=False)
os.replace(tmp, "/opt/pbs-relay/data/pbs-grid.json")
