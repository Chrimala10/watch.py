import json, urllib.request, pathlib
U = "https://www.tikwm.com/api/user/info?unique_id=gajabordessa"
r = urllib.request.urlopen(urllib.request.Request(U, headers={"User-Agent": "Mozilla/5.0"}), timeout=30)
s = json.load(r)["data"]["stats"]
p = pathlib.Path("stato.json")
old = json.loads(p.read_text()) if p.exists() else {}
now = {"videoCount": s["videoCount"], "heartCount": s["heartCount"], "followerCount": s["followerCount"]}
print("prima:", old, "adesso:", now)
p.write_text(json.dumps(now))
if old.get("videoCount") != now["videoCount"]:
    print("CAMBIO:", old.get("videoCount"), "->", now["videoCount"])
    raise SystemExit(1)
