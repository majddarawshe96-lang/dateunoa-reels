"""Build Buffer createPost batches for @dateunoa (Instagram, Facebook, X).

Usage: python3 tools/buffer_plan.py <content_module> <out_dir> [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--ig-from YYYY-MM-DD] [--batch 10]
  content_module: python file in content/ defining DAYS and PROMO_CAPTIONS (see content/week1.py)
Writes <out_dir>/plan.json (every post) and <out_dir>/batch_NN.json, each {"mutation": ..., "variables": ...}
ready to send with the Buffer execute_mutation tool (one API request per batch).
"""
import importlib.util
import json
import sys
from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from captions import caption, PROMO_CAPTIONS as DEFAULT_PROMO  # noqa: E402

SLOTS = ["08:15", "09:45", "11:15", "12:45", "14:00", "15:45", "17:15", "18:45", "20:15", "21:45"]
RAW = "https://raw.githubusercontent.com/majddarawshe96-lang/dateunoa-reels/main/reels/"
CH = {"instagram": "6ac7b0a16a5c39ccb651ff2c", "facebook": "6ada5f7b778b240e2f9111b7", "twitter": "6ac7b0f46a5c39ccb6520e30"}
TZ = ZoneInfo("Asia/Jerusalem")


def due(day, hhmm):
    dt = datetime.fromisoformat(f"{day}T{hhmm}:00").replace(tzinfo=TZ)
    return dt.isoformat()


def build(days, promo_captions, d_from=None, d_to=None, ig_from=None, nets=("instagram", "facebook", "twitter")):
    plan = []
    for d, v in days.items():
        if (d_from and d < d_from) or (d_to and d > d_to):
            continue
        n0 = date.fromisoformat(d).toordinal() * 10
        items = [(post[0], post[2], f"{RAW}{d}/dq_{i + 1:02d}.mp4", None) for i, post in enumerate(v["posts"])]
        items.insert(4, ("PROMO", None, f"{RAW}promo/promo_{v['promo']}.mp4", promo_captions[v["promo"]]))
        for si, (p, h, url, pt) in enumerate(items):
            for net in nets:
                if net == "instagram" and ig_from and d < ig_from:
                    continue
                plan.append({"day": d, "time": SLOTS[si], "dueAt": due(d, SLOTS[si]), "net": net,
                             "channelId": CH[net], "pillar": p, "video": url,
                             "text": caption(p, h, net, n0 + si, pt)})
    return plan


def inp(x):
    d = {"channelId": x["channelId"], "mode": "customScheduled", "dueAt": x["dueAt"], "schedulingType": "automatic",
         "text": x["text"], "assets": [{"video": {"url": x["video"]}}]}
    if x["net"] == "instagram":
        d["metadata"] = {"instagram": {"type": "reel", "shouldShareToFeed": True}}
    if x["net"] == "facebook":
        d["metadata"] = {"facebook": {"type": "reel"}}
    return d


def batch(items, name):
    decl, parts, var = [], [], {}
    for i, x in enumerate(items):
        decl.append(f"$i{i}:CreatePostInput!")
        parts.append(f"p{i}:createPost(input:$i{i}){{__typename ...on MutationError{{message}}}}")
        var[f"i{i}"] = inp(x)
    return {"mutation": f"mutation {name}({','.join(decl)}){{{' '.join(parts)}}}", "variables": var}


def main():
    a = sys.argv[1:]
    mod_path, out = Path(a.pop(0)), Path(a.pop(0))
    opts = dict(zip(a[::2], a[1::2]))
    spec = importlib.util.spec_from_file_location("content", mod_path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    plan = build(m.DAYS, getattr(m, "PROMO_CAPTIONS", DEFAULT_PROMO), opts.get("--from"), opts.get("--to"), opts.get("--ig-from"))
    out.mkdir(parents=True, exist_ok=True)
    json.dump(plan, open(out / "plan.json", "w"), ensure_ascii=False, indent=1)
    size = int(opts.get("--batch", 10))
    for k in range(0, len(plan), size):
        json.dump(batch(plan[k:k + size], f"B{k // size:02d}"), open(out / f"batch_{k // size:02d}.json", "w"), ensure_ascii=False)
    print(len(plan), "posts in", (len(plan) + size - 1) // size, "batches")


if __name__ == "__main__":
    main()
