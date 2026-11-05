#!/usr/bin/env python3
# Coupe les lectures Jellyfin restées en pause trop longtemps (flux inutile).
# La personne reçoit un message, la lecture s'arrête ; Jellyfin garde la position pour reprendre.
# Usage : jf-pause-stop.py [--dry-run]   (cron toutes les 30 min, CT 102)
import datetime, json, sys, urllib.parse, urllib.request

JF = "http://192.168.1.102:8096"
PAUSE_MAX_MIN = 120      # au-delà : arrêt lecture / transcodage
DECONNEXION_MIN = 360    # au-delà, si le client n'est pas pilotable : déconnexion de l'appareil
DRY = "--dry-run" in sys.argv
KEY = open("/root/.jellyfin-collections-key").read().strip()
AUTH = f'MediaBrowser Token="{KEY}"'  # Jellyfin 12 refuse X-Emby-Token


def jf(method, path, body=None, **params):
    url = JF + path + ("?" + urllib.parse.urlencode(params) if params else "")
    data = json.dumps(body).encode() if body is not None else (b"" if method == "POST" else None)
    req = urllib.request.Request(url, method=method, data=data,
                                 headers={"Authorization": AUTH, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
        return json.loads(raw) if raw else None


now = datetime.datetime.now(datetime.timezone.utc)
for s in jf("GET", "/Sessions", activeWithinSeconds=3600):
    np, ps = s.get("NowPlayingItem"), s.get("PlayState") or {}
    if not np or not ps.get("IsPaused") or not s.get("LastPausedDate"):
        continue
    depuis = now - datetime.datetime.fromisoformat(s["LastPausedDate"].replace("Z", "+00:00")[:26] + "+00:00")
    minutes = int(depuis.total_seconds() // 60)
    if minutes < PAUSE_MAX_MIN:
        continue
    qui = f"{s.get('UserName')} / {s.get('Client')} « {np.get('Name')} » en pause depuis {minutes} min"
    pilotable, transcode = s.get("SupportsRemoteControl"), s.get("TranscodingInfo")
    if not pilotable and not transcode:
        if minutes < DECONNEXION_MIN or not s.get("DeviceId"):
            print(f"{now:%Y-%m-%d %H:%M} non pilotable, on attend {DECONNEXION_MIN} min : {qui}")
            continue
        print(f"{now:%Y-%m-%d %H:%M} {'(simulation) ' if DRY else ''}déconnecte l'appareil {s.get('DeviceName')} : {qui}")
        if not DRY:  # la personne devra se reconnecter ; sa position dans le film est gardée
            jf("DELETE", "/Devices", id=s["DeviceId"])
        continue
    print(f"{now:%Y-%m-%d %H:%M} {'(simulation) ' if DRY else ''}coupe {qui}"
          f"{' [arrêt lecture]' if pilotable else ''}{' [arrêt transcodage]' if transcode else ''}")
    if DRY:
        continue
    if pilotable:
        try:
            jf("POST", f"/Sessions/{s['Id']}/Message", body={"Header": "Lecture arrêtée",
               "Text": f"Pause de plus de {PAUSE_MAX_MIN} min : flux coupé. Tu peux reprendre où tu en étais.",
               "TimeoutMs": 15000})
        except Exception:
            pass  # certains clients n'affichent pas les messages
        jf("POST", f"/Sessions/{s['Id']}/Playing/Stop")
    if transcode:  # libère FFmpeg même si le client ne réagit pas
        jf("DELETE", "/Videos/ActiveEncodings", deviceId=s.get("DeviceId"), playSessionId=ps.get("PlaySessionId", ""))
