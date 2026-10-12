#!/usr/bin/env python3
"""Generate the artifact gallery served by GitHub Pages.

Two jobs:

    python3 tools/gallery.py --stills    cut one representative still per video into
                                         gallery/stills/ and write gallery/manifest.json
    python3 tools/gallery.py             write index.html at the repository root

GitHub's own file view renders images, PDFs, and 3D models but not video, so a committed
.mp4 can only be downloaded from there. This page exists so the videos can be watched, and
so each one sits beside the Manim script that generated it.

Stills are picked by content, not by a fixed timestamp: 24 frames are sampled in a single
pass, scored by how many pixels differ from that video's own background and by how widely
those pixels are spread across the frame, and the best one is cut at full size. Manim
builds a scene up over its runtime, so an early frame is often an empty canvas.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html
import json
import re
import pathlib
import subprocess
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"
GALLERY = ROOT / "gallery"
STILLS = GALLERY / "stills"
MANIFEST = GALLERY / "manifest.json"

REPO = "jdluu/ConceptCast-results"
RELEASE = f"https://github.com/{REPO}/releases/tag/artifacts-v1"

ARM_ORDER = ["A", "B", "C"]
ARM_TITLES = {
    "A": "Arm A, monolithic baseline",
    "B": "Arm B, monolithic with repair",
    "C": "Arm C, agent council",
}
ARM_NOTES = {
    "A": "One generation from one prompt, rendered exactly as produced. No retrieval, no "
         "verification, no repair.",
    "B": "One generation, then AST checks, a sandboxed render, and a search-and-replace "
         "repair loop.",
    "C": "The full council: Analyst, Architect, and Animator, with the check and repair "
         "stages around them.",
}
TOPIC_ORDER = ["derivative", "backpropagation", "fourier", "doppler", "eigenvectors"]
TOPIC_LABELS = {
    "derivative": "Derivative",
    "backpropagation": "Backpropagation",
    "fourier": "Fourier transform",
    "doppler": "Doppler effect",
    "eigenvectors": "Eigenvectors",
}


def slug(topic: str) -> str:
    """Map a full topic string from index.csv onto its short slug."""
    lowered = topic.lower()
    for candidate in TOPIC_ORDER:
        if lowered.startswith(candidate):
            return candidate
    raise ValueError(f"unrecognized topic: {topic!r}")


# --------------------------------------------------------------------------- stills

def _duration(video: pathlib.Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "json", str(video)], capture_output=True, text=True).stdout
    return float(json.loads(out)["format"]["duration"])


def _score_tile(tile: bytes, w: int = 32, h: int = 18) -> tuple[float, int]:
    """Content of one sampled frame: pixels far from its own background, plus spread."""
    if len(tile) < w * h:
        return -1.0, 0
    mode = Counter(tile).most_common(1)[0][0]
    far = [i for i, b in enumerate(tile) if abs(b - mode) > 24]
    if not far:
        return 0.0, mode
    blocks = {(i % w) // 8 * 6 + (i // w) // 5 for i in far}
    return len(far) / (w * h) + 0.6 * len(blocks) / 16, mode


def build_stills(force: bool = False) -> dict:
    """Cut one still per video and return the manifest."""
    STILLS.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    for i, r in enumerate(rows, 1):
        job = job_name(r)
        video = ROOT / "artifacts" / r["video"]
        still = STILLS / f"{job}.jpg"
        if force or not still.exists():
            dur = _duration(video)
            step = max(1, int(dur * 15) // 24)
            buf = subprocess.run(
                ["ffmpeg", "-v", "error", "-i", str(video),
                 "-vf", f"select='not(mod(n\\,{step}))',scale=32:18,tile=6x4",
                 "-frames:v", "1", "-pix_fmt", "gray", "-f", "rawvideo", "-"],
                capture_output=True).stdout
            best_i, best_score, bg = 0, -1.0, 0
            for k in range(min(24, len(buf) // 576)):
                score, mode = _score_tile(buf[k * 576:(k + 1) * 576])
                if score > best_score:
                    best_i, best_score, bg = k, score, mode
            at = min(best_i * step / 15.0, max(dur - 0.1, 0.02))
            subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{at:.3f}", "-i", str(video),
                            "-frames:v", "1", "-vf", "scale=480:270", "-pix_fmt", "yuvj420p",
                            "-q:v", "5", "-strict", "unofficial", "-y", str(still)],
                           capture_output=True)
            manifest[job] = {
                "still": f"gallery/stills/{job}.jpg",
                "duration": round(dur, 2),
                "video_bytes": video.stat().st_size,
                "still_bytes": still.stat().st_size if still.exists() else 0,
                "frame_at": round(at, 2),
                "content": round(max(best_score, 0), 3),
                "bg_luma": bg,
            }
        if i % 25 == 0:
            print(f"  stills {i}/{len(rows)}", file=sys.stderr)
    MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    missing = [job_name(r) for r in rows if job_name(r) not in manifest]
    if missing:
        raise SystemExit(f"stills missing for {len(missing)} jobs, e.g. {missing[0]}")
    return manifest


# --------------------------------------------------------------------------- data

def job_name(row: dict) -> str:
    return str(pathlib.PurePosixPath(row["code_file"]).parent.name)


def load_rows() -> list[dict]:
    with (ARTIFACTS / "index.csv").open(newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("code_file")]


def load_jobs() -> list[dict]:
    manifest = json.loads(MANIFEST.read_text())
    jobs = []
    for r in load_rows():
        job = job_name(r)
        m = manifest[job]
        topic = slug(r["topic"])
        folder = str(pathlib.PurePosixPath(r["code_file"]).parent)   # arm_A/<job>, as in index.csv
        jobs.append({
            "job": job,
            "arm": r["arm"],
            "topic": topic,
            "topic_label": TOPIC_LABELS[topic],
            "model": r["model"].split("/")[-1],
            "rep": r["rep"],
            "seq": int(r["job_seq"]),
            "duration": m["duration"],
            "video_bytes": m["video_bytes"],
            "video": f"artifacts/{r['video']}",
            "code": f"artifacts/{r['code_file']}",
            "still": m["still"],
            "folder": f"artifacts/{folder}",
            "github_folder": f"https://github.com/{REPO}/tree/main/artifacts/{folder}",
            "github_script": f"https://github.com/{REPO}/blob/main/artifacts/{folder}/scene.py",
        })
    jobs.sort(key=lambda j: (ARM_ORDER.index(j["arm"]), j["topic"], j["model"], j["rep"], j["seq"]))
    # other runs of the same topic and model, so a reader can compare arms
    for j in jobs:
        j["compare"] = [{"job": o["job"], "arm": o["arm"], "rep": o["rep"]} for o in jobs
                        if o["job"] != j["job"] and o["topic"] == j["topic"]
                        and o["model"] == j["model"]]
        j["search"] = " ".join([j["job"], f"arm {j['arm']}", f"arm{j['arm']}", j["topic"],
                                j["topic_label"], j["model"], f"seq{j['seq']}",
                                f"rep{j['rep']}"]).lower()
    return jobs


# --------------------------------------------------------------------------- page

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ConceptCast benchmark artifacts</title>
<meta name="description" content="Rendered videos from the ConceptCast ablation benchmark, each beside the Manim script that generated it.">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; media-src 'self'; font-src 'self'; style-src 'self'; script-src 'self' __CSP_SCRIPT_HASH__; connect-src 'self'; base-uri 'none'; form-action 'none'">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%233fa796'/%3E%3Cpath d='M13 10l9 6-9 6z' fill='%230c0f13'/%3E%3C/svg%3E">
<link rel="preload" href="gallery/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="gallery/fonts/geist-mono-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face{font-family:Geist;src:url(gallery/fonts/geist-latin.woff2)format("woff2");font-weight:100 900;font-display:swap}
@font-face{font-family:"Geist Mono";src:url(gallery/fonts/geist-mono-latin.woff2)format("woff2");font-weight:100 900;font-display:swap}
:root{
  --bg:#0c0f13; --panel:#141920; --panel-2:#1a2029; --line:#2a323d; --frame:#333d4a;
  --fg:#e7eaee; --muted:#98a2b0; --accent:#3fa796;
  /* radius scale: 10px for every control and container, 14px for the dialog panel,
     6px for focus outlines. One documented rule, applied everywhere. */
  --radius:10px; --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px rgba(0,0,0,.28);
  --sans:Geist,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"Geist Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme:light){
  :root{
    --bg:#f6f7f8; --panel:#ffffff; --panel-2:#f0f2f4; --line:#dfe3e8; --frame:#ccd3db;
    --fg:#14181d; --muted:#5c6673; --accent:#0f766e;
    --shadow:0 1px 2px rgba(16,24,32,.06), 0 8px 24px rgba(16,24,32,.08);
  }
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 var(--sans)}
a{color:inherit;text-decoration:none}
a:hover{color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:6px}
.wrap{max-width:1280px;margin:0 auto;padding:0 20px}
.skip{position:absolute;left:-9999px}
.skip:focus{left:12px;top:12px;background:var(--panel);padding:8px 12px;border-radius:var(--radius);z-index:9}

.bar{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);
     backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar .wrap{display:flex;align-items:center;gap:16px;min-height:64px;flex-wrap:nowrap}
.brand{font-weight:600;letter-spacing:-.01em;white-space:nowrap;font-size:15px}
.brand span{display:block;color:var(--muted);font-weight:400;font-size:12px;line-height:1.2}
.tools{display:flex;align-items:center;gap:10px;margin-left:auto;min-width:0}
input[type=search],select{font:inherit;color:var(--fg);background:var(--panel);
     border:1px solid var(--line);border-radius:var(--radius);padding:0 10px;height:38px;min-width:0}
input[type=search]{width:230px}
#topic{width:132px}
#model{width:200px}
input[type=search]::placeholder{color:var(--muted);opacity:1}
.seg{display:flex;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;background:var(--panel);height:38px}
.seg button{font:inherit;color:var(--muted);background:none;border:0;padding:0 13px;cursor:pointer;
            display:inline-flex;align-items:center}
.seg button+button{border-left:1px solid var(--line)}
.seg button[aria-pressed=true]{background:var(--panel-2);color:var(--fg)}
.seg button .narrow{display:none}
.count{color:var(--muted);font-size:13px;white-space:nowrap;font-variant-numeric:tabular-nums;
       text-align:right;min-width:86px}

.intro{padding:40px 0 8px;max-width:70ch}
h1{font-size:30px;line-height:1.15;letter-spacing:-.02em;margin:0 0 12px;font-weight:600}
.intro p{margin:0 0 14px;color:var(--muted)}
.facts{font-family:var(--mono);font-size:12.5px;color:var(--muted);letter-spacing:.01em}
.jump{display:flex;gap:18px;flex-wrap:wrap;font-size:14px;margin-top:4px}
.jump a{color:var(--accent)}

section.arm{padding:34px 0 6px;border-top:1px solid var(--line);margin-top:26px}
section.arm[hidden]{display:none}
h2{font-size:19px;letter-spacing:-.01em;margin:0 0 6px;font-weight:600}
.armnote{margin:0 0 20px;color:var(--muted);max-width:72ch}
.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.item{display:flex;flex-direction:column;gap:8px;height:100%}
.item[hidden]{display:none}
/* one link per card: the still and the title share it, so the tap target is the whole top
   of the card and a keyboard user gets a single stop per job */
.shot{position:relative;display:block}
.shot img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;
      background:var(--panel-2);border:1px solid var(--frame);border-radius:var(--radius)}
.play{position:absolute;top:0;left:0;right:0;aspect-ratio:16/9;display:grid;place-items:center;opacity:.75}
/* a scrim disc, so the affordance stays visible on bright thumbnails as well as dark ones */
.play::before{content:"";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
        width:54px;height:54px;border-radius:50%;background:rgba(6,8,11,.6);
        border:1px solid rgba(255,255,255,.22)}
.play::after{content:"";width:0;height:0;border-style:solid;border-width:11px 0 11px 18px;
        border-color:transparent transparent transparent #fff;margin-left:4px;
        filter:drop-shadow(0 1px 3px rgba(0,0,0,.6))}
.shot:hover .play,.shot:focus-visible .play{opacity:1}
@media (prefers-reduced-motion:no-preference){
  .play{transition:opacity .14s ease}
  .shot img{transition:transform .18s ease}
  .shot:hover img{transform:scale(1.025)}
}
.title{display:block;margin-top:9px;font-size:14.5px;font-weight:500;letter-spacing:-.005em;line-height:1.35}
.facts2{color:var(--muted);font-size:12.5px}
.jobid{font-family:var(--mono);font-size:11.5px;color:var(--muted);line-height:1.35;
       overflow-wrap:anywhere;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
       overflow:hidden}
.actions{display:flex;gap:8px;margin-top:auto;padding-top:2px}
.chip{align-self:flex-start;color:var(--muted);border:1px solid var(--line);border-radius:var(--radius);
      padding:6px 12px;line-height:1.3;font-size:12.5px}
.chip:hover{color:var(--accent);border-color:var(--accent)}
.reset{font:inherit;font-size:13px;color:var(--fg);background:var(--panel-2);
       border:1px solid var(--line);border-radius:var(--radius);padding:0 12px;height:38px;cursor:pointer}
.reset:hover{border-color:var(--accent);color:var(--accent)}
.reset:active{transform:translateY(1px)}

.empty{display:none;padding:56px 0;text-align:center;color:var(--muted)}
.empty.on{display:block}
.empty p{margin:0 0 14px}
button.ghost{font:inherit;color:var(--fg);background:var(--panel);border:1px solid var(--line);
             border-radius:var(--radius);padding:8px 14px;cursor:pointer}
button.ghost:active{transform:translateY(1px)}

footer{border-top:1px solid var(--line);margin-top:44px;padding:22px 0 60px;color:var(--muted);font-size:13px}
footer p{margin:0 0 8px;max-width:80ch}

dialog{border:1px solid var(--line);border-radius:14px;background:var(--panel);color:var(--fg);
       padding:0;max-width:940px;width:calc(100% - 32px);box-shadow:var(--shadow)}
dialog::backdrop{background:rgba(4,6,9,.72)}
.dhead{display:flex;align-items:flex-start;gap:12px;padding:14px 18px;border-bottom:1px solid var(--line)}
.dhead h2{font-size:16px;font-weight:600;letter-spacing:-.01em;margin:0 0 3px}
.djob{font-family:var(--mono);font-size:12px;color:var(--muted);word-break:break-all}
.dclose{margin-left:auto;background:none;border:0;color:var(--muted);font-size:22px;line-height:1;
        cursor:pointer;padding:4px 8px;border-radius:var(--radius)}
.dclose:hover{color:var(--fg)}
.dgrid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:20px;padding:18px}
video{width:100%;aspect-ratio:16/9;background:#000;border-radius:var(--radius);display:block}
.dfacts{font-family:var(--mono);font-size:12.5px;color:var(--muted);margin:0 0 12px}
.dnote{margin:0 0 14px;color:var(--muted);font-size:14px}
.dlinks{display:flex;flex-wrap:wrap;gap:16px;margin-bottom:16px;font-size:14px}
.dlinks a{color:var(--accent)}
.dlinks button{font:inherit;font-size:14px;color:var(--accent);background:none;border:0;padding:0;
               cursor:pointer;text-align:left}
.cmp h3{font-size:12.5px;color:var(--muted);margin:0 0 8px;font-weight:500}
.cmp ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.cmp a{font-family:var(--mono);font-size:12px;border:1px solid var(--line);border-radius:var(--radius);
       padding:5px 9px;background:var(--panel-2)}
.dcode{border-top:1px solid var(--line)}
.dcode summary{padding:12px 18px;cursor:pointer;color:var(--muted);font-size:13.5px}
.dcode summary:hover{color:var(--fg)}
.codewrap{max-height:340px;overflow:auto;border-top:1px solid var(--line);background:var(--bg)}
pre{margin:0;padding:14px 18px;font:12.5px/1.55 var(--mono);overflow-x:auto;white-space:pre}
.skeleton{padding:14px 18px;display:grid;gap:7px}
.skeleton span{height:10px;border-radius:4px;background:var(--panel-2);display:block}
@media (prefers-reduced-motion:no-preference){.skeleton span{animation:pulse 1.1s ease-in-out infinite}}
@keyframes pulse{0%,100%{opacity:.45}50%{opacity:.9}}
.dnav{display:flex;gap:10px;justify-content:space-between;align-items:center;padding:12px 18px;
      border-top:1px solid var(--line);font-size:13.5px}
.dnav button{font:inherit;background:var(--panel-2);color:var(--fg);border:1px solid var(--line);
             border-radius:var(--radius);padding:7px 12px;cursor:pointer}
.dnav button:disabled{opacity:.4;cursor:default}
.dnav .hint{color:var(--muted);font-size:12.5px}

@media (max-width:1200px){
  .bar .wrap{flex-wrap:wrap;padding-top:10px;padding-bottom:10px;min-height:0}
  .tools{width:100%;margin-left:0;flex-wrap:wrap}
  .count{margin-left:auto}
}
@media (max-width:760px){
  input[type=search]{flex:1 1 auto;width:auto;min-width:0}
  .tools{gap:8px}
  .count{margin-left:0;text-align:left;min-width:0;flex:0 0 auto}
  .seg{width:auto}
  .seg button{padding:0 12px}
  .seg button .wide{display:none}
  .seg button .narrow{display:inline}
  #topic,#model{flex:1 1 0;width:auto;min-width:96px}
  .brand span{display:none}
  /* iOS zooms the whole page when a focused control renders under 16px, and 44px is the
     smallest comfortable thumb target */
  input[type=search],select{font-size:16px;height:44px}
  .seg{height:44px}
  .reset{height:44px;padding:0 14px}
  /* the per-card chips are redundant here: the whole card opens the detail view, which
     carries the same actions at a comfortable size */
  .chip{display:none}
  /* a solid bar: the backdrop blur costs frames and battery on a phone */
  .bar{background:var(--bg);backdrop-filter:none}
  .dclose{font-size:26px;padding:9px 12px;min-width:44px;min-height:44px}
  .dlinks{gap:10px 18px}
  .dlinks a,.dlinks button{display:inline-block;padding:10px 0;min-height:44px}
  .dnav button{padding:12px 16px}
  .cmp a{padding:9px 11px}
  .dcode summary{padding:14px 18px}
  .intro{padding-top:26px}
  h1{font-size:24px}
  .grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
  .dgrid{grid-template-columns:1fr;gap:16px;padding:14px}
  dialog{padding:0;width:100%;max-width:none;height:100%;max-height:none;border-radius:0;border:0}
  .dnav .hint{display:none}
}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to the videos</a>

<header class="bar">
  <div class="wrap">
    <div class="brand">ConceptCast<span>benchmark artifacts</span></div>
    <div class="tools">
      <label class="skip" for="filter">Filter jobs</label>
      <input type="search" id="filter" placeholder="Filter jobs" autocomplete="off"
             title="Matches job name, topic, model, arm, repetition or job number">
      <div class="seg" role="group" aria-label="Filter by arm">
        <button type="button" data-arm="all" aria-pressed="true"><span class="wide">All arms</span><span class="narrow">All</span></button>
        <button type="button" data-arm="A" aria-pressed="false">A</button>
        <button type="button" data-arm="B" aria-pressed="false">B</button>
        <button type="button" data-arm="C" aria-pressed="false">C</button>
      </div>
      <label class="skip" for="topic">Filter by topic</label>
      <select id="topic">
        <option value="all">All topics</option>
__TOPIC_OPTIONS__
      </select>
      <label class="skip" for="model">Filter by model</label>
      <select id="model">
        <option value="all">All models</option>
__MODEL_OPTIONS__
      </select>
      <span class="count" id="count" aria-live="polite"></span>
      <button type="button" class="reset" id="reset" hidden>Clear filters</button>
    </div>
  </div>
</header>

<main id="main" class="wrap">
  <div class="intro">
    <h1>Rendered videos from the ConceptCast benchmark</h1>
    <p>Every job in the ablation study that produced a video, each one beside the Manim
       script that generated it. Open a video to watch it, read its code, and compare the
       same topic and model across arms.</p>
    <p class="facts">__TOTAL_JOBS__ videos &middot; __TOTAL_MODELS__ models &middot; 5 topics &middot; __TOTAL_MB__ MB &middot; __TOTAL_DUR__ minutes of animation</p>
    <div class="jump">
      <a href="__RELEASE__">Bulk download</a>
      <a href="__REPO__">Repository</a>
      <a href="artifacts/README.md">Artifact layout</a>
    </div>
  </div>

__SECTIONS__

  <div class="empty" id="empty">
    <p>Nothing matches those filters.</p>
    <button class="ghost" type="button" id="clear">Clear filters</button>
  </div>
</main>

<footer class="wrap">
  <p>Videos are served from this repository by GitHub Pages. GitHub's own file view cannot
     play a committed video, which is why this page exists. Players load nothing until you
     press play.</p>
  <p>Generated from <span class="facts">artifacts/index.csv</span> and
     <span class="facts">gallery/manifest.json</span> by
     <span class="facts">tools/gallery.py</span>.</p>
</footer>

<dialog id="detail" aria-labelledby="dname">
  <div class="dhead">
    <div>
      <h2 id="dname">job</h2>
      <div class="djob" id="djob"></div>
    </div>
    <button class="dclose" type="button" id="dclose" aria-label="Close">&times;</button>
  </div>
  <div class="dgrid">
    <div><video id="dvideo" controls preload="metadata" playsinline></video></div>
    <div>
      <p class="dfacts" id="dfacts"></p>
      <p class="dnote" id="dnote"></p>
      <div class="dlinks">
        <a id="dgh" href="#">Open job folder</a>
        <a id="dvideo-raw" href="#">Download video</a>
        <a id="dscript" href="#" target="_blank" rel="noopener">Open script</a>
        <button type="button" id="dcopy">Copy link</button>
      </div>
      <div class="cmp" id="dcmpwrap">
        <h3>Other runs of this topic and model</h3>
        <ul id="dcmp"></ul>
      </div>
    </div>
  </div>
  <details class="dcode">
    <summary>Manim script <span id="dsize"></span></summary>
    <div class="codewrap">
      <div class="skeleton" id="dskeleton"><span></span><span></span><span></span><span></span><span></span><span></span></div>
      <pre hidden><code id="dcode"></code></pre>
    </div>
  </details>
  <div class="dnav">
    <button type="button" id="dprev">&larr; Previous</button>
    <span class="hint">Left and right arrows move between jobs, Esc closes</span>
    <button type="button" id="dnext">Next &rarr;</button>
  </div>
</dialog>

<script id="jobs" type="application/json">__JOBS__</script>
<script>
(function () {
  var JOBS = JSON.parse(document.getElementById('jobs').textContent);
  var ARM_NOTES = __ARM_NOTES__;
  var items = Array.prototype.slice.call(document.querySelectorAll('.item'));
  var sections = Array.prototype.slice.call(document.querySelectorAll('section.arm'));
  var filter = document.getElementById('filter');
  var topicSel = document.getElementById('topic');
  var modelSel = document.getElementById('model');
  var count = document.getElementById('count');
  var reset = document.getElementById('reset');
  var empty = document.getElementById('empty');
  var arm = 'all';
  var visible = items.slice();

  function matches(el) {
    var q = filter.value.trim().toLowerCase();
    return (!q || el.dataset.search.indexOf(q) !== -1)
        && (arm === 'all' || el.dataset.arm === 'arm_' + arm)
        && (topicSel.value === 'all' || el.dataset.topic === topicSel.value)
        && (modelSel.value === 'all' || el.dataset.model === modelSel.value);
  }

  function apply() {
    visible = [];
    items.forEach(function (el) {
      var ok = matches(el);
      el.hidden = !ok;
      if (ok) visible.push(el);
    });
    sections.forEach(function (s) {
      s.hidden = !s.querySelector('.item:not([hidden])');
    });
    var n = visible.length, total = items.length;
    count.textContent = n === total ? total + ' videos' : n + ' of ' + total;
    empty.classList.toggle('on', n === 0);
    // one Clear filters control is visible at a time: in the bar while results remain,
    // and in the empty state when nothing matches
    var filtered = filter.value.trim() !== '' || arm !== 'all'
                || topicSel.value !== 'all' || modelSel.value !== 'all';
    reset.hidden = !filtered || n === 0;
  }
  function clearAll() {
    filter.value = '';
    topicSel.value = 'all';
    modelSel.value = 'all';
    arm = 'all';
    document.querySelectorAll('.seg button').forEach(function (o) {
      o.setAttribute('aria-pressed', String(o.dataset.arm === 'all'));
    });
    apply();
  }

  filter.addEventListener('input', apply);
  topicSel.addEventListener('change', apply);
  modelSel.addEventListener('change', apply);
  document.querySelectorAll('.seg button').forEach(function (b) {
    b.addEventListener('click', function () {
      arm = b.dataset.arm;
      document.querySelectorAll('.seg button').forEach(function (o) {
        o.setAttribute('aria-pressed', String(o === b));
      });
      apply();
    });
  });
  document.getElementById('clear').addEventListener('click', clearAll);
  reset.addEventListener('click', clearAll);

  var dlg = document.getElementById('detail');
  var dvideo = document.getElementById('dvideo');
  var dname = document.getElementById('dname');
  var dfacts = document.getElementById('dfacts');
  var dnote = document.getElementById('dnote');
  var dcmp = document.getElementById('dcmp');
  var dcmpwrap = document.getElementById('dcmpwrap');
  var dsize = document.getElementById('dsize');
  var dcode = document.getElementById('dcode');
  var dpre = dcode.parentElement;
  var dskel = document.getElementById('dskeleton');
  var details = dlg.querySelector('.dcode');
  var current = null;
  var codeCache = {};

  function fmtBytes(b) {
    return b > 1048576 ? (b / 1048576).toFixed(1) + ' MB' : Math.round(b / 1024) + ' KB';
  }
  function fmtDur(s) {
    return s >= 60 ? Math.floor(s / 60) + 'm ' + Math.round(s % 60) + 's' : s.toFixed(1) + 's';
  }

  function loadCode(job) {
    if (codeCache[job.code]) {
      dskel.hidden = true; dpre.hidden = false;
      dcode.textContent = codeCache[job.code];
      return;
    }
    dskel.hidden = false; dpre.hidden = true;
    dcode.textContent = '';
    fetch(job.code).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.text();
    }).then(function (text) {
      codeCache[job.code] = text;
      if (current !== job) return;
      dskel.hidden = true; dpre.hidden = false;
      dcode.textContent = text;
    }).catch(function () {
      if (current !== job) return;
      dskel.hidden = true; dpre.hidden = false;
      dcode.textContent = 'This script could not be loaded here. Use "Open script" above.';
    });
  }

  function fill(job) {
    current = job;
    dname.textContent = job.topic_label + ' \u00b7 ' + job.model;
    document.getElementById('djob').textContent = job.job;
    dsize.textContent = '';
    dfacts.textContent = 'arm ' + job.arm + ' \u00b7 rep ' + job.rep + ' \u00b7 job ' + job.seq
                       + ' \u00b7 ' + fmtDur(job.duration) + ' \u00b7 ' + fmtBytes(job.video_bytes);
    dnote.textContent = ARM_NOTES[job.arm];
    dvideo.poster = job.still;
    dvideo.src = job.video;
    document.getElementById('dgh').href = job.github_folder;
    document.getElementById('dvideo-raw').href = job.video;
    document.getElementById('dscript').href = job.github_script;
    details.open = false;
    dcmp.replaceChildren();          // clearing only; children are built with createElement
    dcmpwrap.hidden = job.compare.length === 0;
    job.compare.forEach(function (o) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#' + o.job;
      a.textContent = 'Arm ' + o.arm + ' rep ' + o.rep;
      a.title = o.job;
      li.appendChild(a);
      dcmp.appendChild(li);
    });
    loadCode(job);
    var i = visible.findIndex(function (el) { return el.dataset.job === job.job; });
    document.getElementById('dprev').disabled = i <= 0;
    document.getElementById('dnext').disabled = i < 0 || i >= visible.length - 1;
  }

  function openJob(name) {
    var job = JOBS[name];
    if (!job) return false;
    fill(job);
    if (!dlg.open) dlg.showModal();
    if (location.hash.slice(1) !== name) history.replaceState(null, '', '#' + name);
    return true;
  }

  function step(delta) {
    var i = visible.findIndex(function (el) { return el.dataset.job === current.job; });
    if (visible[i + delta]) openJob(visible[i + delta].dataset.job);
  }

  document.getElementById('dclose').addEventListener('click', function () { dlg.close(); });
  var copyBtn = document.getElementById('dcopy');
  copyBtn.addEventListener('click', function () {
    var url = location.origin + location.pathname + '#' + current.job;
    function done(ok) {
      copyBtn.textContent = ok ? 'Link copied' : 'Copy failed';
      setTimeout(function () { copyBtn.textContent = 'Copy link'; }, 1600);
    }
    if (navigator.clipboard && location.protocol !== 'file:') {
      navigator.clipboard.writeText(url).then(function () { done(true); },
                                               function () { done(false); });
    } else {
      done(false);
    }
  });
  document.getElementById('dprev').addEventListener('click', function () { step(-1); });
  document.getElementById('dnext').addEventListener('click', function () { step(1); });
  // Cleanup must not depend on the close event alone: a programmatic close() does not
  // always deliver it, while Esc, the backdrop and the button all remove the open
  // attribute. Watching the attribute covers every path and is safe to run twice.
  function cleanup() {
    if (dvideo.hasAttribute('src')) {
      dvideo.pause();
      dvideo.removeAttribute('src');
      dvideo.load();
    }
    if (location.hash) history.replaceState(null, '', location.pathname + location.search);
  }
  dlg.addEventListener('close', cleanup);
  new MutationObserver(function () { if (!dlg.open) cleanup(); })
    .observe(dlg, { attributes: true, attributeFilter: ['open'] });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  dcmp.addEventListener('click', function (e) {
    var a = e.target.closest('a');
    if (!a) return;
    e.preventDefault();
    openJob(a.getAttribute('href').slice(1));
  });
  document.addEventListener('keydown', function (e) {
    if (!dlg.open) {
      if (e.key === '/' && document.activeElement !== filter) { e.preventDefault(); filter.focus(); }
      return;
    }
    if (e.key === 'ArrowRight') step(1);
    else if (e.key === 'ArrowLeft') step(-1);
  });
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var name = a.getAttribute('href').slice(1);
      if (JOBS[name]) { e.preventDefault(); openJob(name); }
    });
  });
  window.addEventListener('hashchange', function () {
    var name = location.hash.slice(1);
    if (name && JOBS[name]) openJob(name);
  });

  apply();
  var start = location.hash.slice(1);
  if (start && JOBS[start]) openJob(start);
})();
</script>
</body>
</html>
"""

ITEM = """      <article class="item" data-job="{job}" data-arm="arm_{arm}" data-topic="{topic}" data-model="{model_plain}" data-search="{search}">
        <a class="shot" href="#{job}" aria-label="{topic_label} &middot; {model}, job {job}">
          <img src="{still}" alt="" width="480" height="270" {loading}>
          <span class="play" aria-hidden="true"></span>
          <span class="title">{topic_label} &middot; {model}</span>
        </a>
        <div class="facts2">arm {arm} &middot; rep {rep} &middot; {duration}</div>
        <div class="jobid" title="{job}">{job}</div>
        <div class="actions"><a class="chip" href="{gh_script}" target="_blank" rel="noopener">script</a><a class="chip" href="{video}">video</a></div>
      </article>
"""

SECTION = """  <section class="arm" data-arm="arm_{arm}">
    <h2>{title}</h2>
    <p class="armnote">{note} {made} of the {attempted} jobs in this arm produced a video.</p>
    <div class="grid">
{items}
    </div>
  </section>
"""


def human_duration(seconds: float) -> str:
    return f"{seconds:.1f}s" if seconds < 60 else f"{int(seconds // 60)}m {seconds % 60:.0f}s"


def build_page(jobs: list[dict], attempted: dict[str, int]) -> str:
    sections = []
    first_card = True
    for arm in ARM_ORDER:
        arm_jobs = [j for j in jobs if j["arm"] == arm]
        chunks = []
        for j in arm_jobs:
            # the first still is the likely LCP element, so it must not be deferred;
            # every other still waits until it is near the viewport
            loading = ('loading="eager" fetchpriority="high"' if first_card
                       else 'loading="lazy" decoding="async"')
            first_card = False
            chunks.append(ITEM.format(
                job=j["job"], arm=arm, topic=j["topic"],
                search=html.escape(j["search"], quote=True), still=j["still"],
                topic_label=html.escape(j["topic_label"]), model=html.escape(j["model"]),
                model_plain=html.escape(j["model"], quote=True),
                rep=j["rep"], duration=human_duration(j["duration"]),
                video=j["video"], gh_script=j["github_script"], loading=loading,
            ))
        sections.append(SECTION.format(
            arm=arm, title=ARM_TITLES[arm], note=ARM_NOTES[arm], made=len(arm_jobs),
            attempted=attempted.get(arm, len(arm_jobs)), items="\n".join(chunks),
        ))

    total_bytes = sum(j["video_bytes"] for j in jobs)
    total_dur = sum(j["duration"] for j in jobs)
    payload = {j["job"]: {k: v for k, v in j.items() if k != "search"} for j in jobs}
    options = "\n".join(f'        <option value="{t}">{TOPIC_LABELS[t]}</option>'
                        for t in TOPIC_ORDER)
    models = sorted({j["model"] for j in jobs})
    model_options = "\n".join(f'        <option value="{html.escape(m, quote=True)}">'
                              f'{html.escape(m)}</option>' for m in models)

    page = (PAGE
            .replace("__SECTIONS__", "\n\n".join(sections))
            .replace("__TOPIC_OPTIONS__", options)
            .replace("__MODEL_OPTIONS__", model_options)
            .replace("__JOBS__", json.dumps(payload, separators=(",", ":"), sort_keys=True))
            .replace("__ARM_NOTES__", json.dumps({a: ARM_NOTES[a] for a in ARM_ORDER}))
            .replace("__TOTAL_JOBS__", str(len(jobs)))
            .replace("__TOTAL_MODELS__", str(len({j["model"] for j in jobs})))
            .replace("__TOTAL_MB__", f"{total_bytes / 1048576:.0f}")
            .replace("__TOTAL_DUR__", f"{total_dur / 60:.0f}")
            .replace("__RELEASE__", RELEASE)
            .replace("__REPO__", f"https://github.com/{REPO}"))
    # The page carries one executable inline script and no inline styles, so the policy can
    # name that script by hash and keep 'unsafe-inline' out of the page entirely.
    # frame-ancestors stays out too: a meta element cannot carry it and the browser logs a
    # console warning, which Lighthouse counts against the page.
    script = re.search(r"<script>(.*?)</script>", page, re.S)
    if not script:
        raise SystemExit("inline script not found, cannot compute the CSP hash")
    digest = hashlib.sha256(script.group(1).encode("utf-8")).digest()
    page = page.replace("__CSP_SCRIPT_HASH__", "'sha256-" + base64.b64encode(digest).decode("ascii") + "'")
    leftover = [tok for tok in page.split() if tok.startswith("__") and tok.endswith("__")]
    if leftover:
        raise SystemExit(f"unreplaced placeholder: {leftover[:3]}")
    return page


def main() -> None:
    ap = argparse.ArgumentParser(description="generate the artifact gallery")
    ap.add_argument("--stills", action="store_true", help="rebuild stills and the manifest")
    ap.add_argument("--force", action="store_true", help="re-cut stills that already exist")
    args = ap.parse_args()

    if args.stills:
        print(f"stills: {len(build_stills(force=args.force))}")
        return

    out = ROOT / "index.html"
    out.write_text(build_page(load_jobs(), {"A": 100, "B": 100, "C": 53}))
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
