import json, pathlib, sys, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"}
SEC = "MS4wLjABAAAAQQFuzfJPRxWh0vf5u3F5oPJwYDj3Jobd6upPQ7oianTJW2Lrp2AscRfSH_ZGFisq"
USER = "gajabordessa"

def get(url, timeout=30):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return r.read()
    except Exception as e:
        print("errore:", url, e)
        return None

def lista():
    for url in (
        "https://www.tiktok.com/api/post/item_list/?count=30&aid=1988&secUid=%s&uniqueId=%s" % (SEC, USER),
        "https://www.tikwm.com/api/user/posts?unique_id=%s&count=35" % USER,
    ):
        raw = get(url)
        if not raw:
            continue
        try:
            d = json.loads(raw.decode("utf-8", "ignore"))
        except Exception:
            print("risposta non JSON:", url)
            continue
        items = d.get("itemList")
        if items is None:
            items = (d.get("data") or {}).get("videos")
        if items is not None:
            ids = []
            for v in items:
                i = v.get("id") or v.get("video_id")
                if i:
                    ids.append(str(i))
            print("fonte:", url.split("/")[2], "- video:", len(ids))
            return ids
    print("nessuna fonte raggiungibile")
    return None

def scarica(vid):
    raw = get("https://www.tikwm.com/api/?url=https://www.tiktok.com/@%s/video/%s" % (USER, vid), 60)
    if not raw:
        return
    try:
        d = json.loads(raw.decode("utf-8", "ignore"))["data"]
    except Exception:
        print("download fallito:", vid)
        return
    for campo, ext in (("hdplay", "mp4"), ("play", "mp4"), ("cover", "jpg")):
        u = d.get(campo)
        if not u:
            continue
        b = get(u, 90)
        if b:
            pathlib.Path("%s.%s" % (vid, ext)).write_bytes(b)
            print("salvato:", vid, campo, len(b), "byte")

p = pathlib.Path("stato.json")
old = json.loads(p.read_text()) if p.exists() else []
now = lista()
if now is None:
    print("stato non aggiornato, esco senza errore")
    sys.exit(0)
nuovi = [i for i in now if i not in old]
print("prima:", len(old), "adesso:", len(now), "nuovi:", len(nuovi))
p.write_text(json.dumps(now, indent=1))
for vid in nuovi:
    scarica(vid)
if nuovi:
    raise SystemExit(1)