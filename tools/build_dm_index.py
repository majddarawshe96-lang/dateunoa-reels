"""Collect every story episode's dm.json into content/stories/dm_index.json, which the dm-bot reads.

Run after adding or editing an episode:  python3 tools/build_dm_index.py
Fails if two episodes use the same keyword (the bot couldn't tell which ending to send),
or if a DM is longer than Instagram's 1000-character message limit.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out, seen, errors = {}, {}, []
for path in sorted(glob.glob(os.path.join(ROOT, "content", "stories", "ep*", "dm.json"))):
    ep = os.path.basename(os.path.dirname(path))
    d = json.load(open(path))
    kw = d["keyword"].strip().upper()
    if kw in seen:
        errors.append(f"keyword {kw} used by both {seen[kw]} and {ep}")
    if len(d["dm"]) > 1000:
        errors.append(f"{ep}: DM is {len(d['dm'])} characters (Instagram limit is 1000)")
    seen[kw] = ep
    out[kw] = {"episode": ep, "dm": d["dm"]}
if errors:
    sys.exit("\n".join(errors))
json.dump({"keywords": out}, open(os.path.join(ROOT, "content", "stories", "dm_index.json"), "w"), indent=1, ensure_ascii=False)
print(f"dm_index.json: {', '.join(f'{k} ({v['episode']})' for k, v in out.items())}")
