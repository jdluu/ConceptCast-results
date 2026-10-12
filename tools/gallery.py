#!/usr/bin/env python3
"""Generate the artifact gallery page served by GitHub Pages.

Reads artifacts/index.csv and writes index.html at the repository root, one card per
job holding an inline player for its video and links to the script beside it.

GitHub's own file view renders images, PDFs, and 3D models but not video, so a
committed .mp4 can only be downloaded from there. This page exists to play them.

Run from the repository root:

    python3 tools/gallery.py
"""

from __future__ import annotations

import csv
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"

ARM_TITLES = {
    "A": "Arm A - Monolithic Baseline",
    "B": "Arm B - Monolithic + Repair",
    "C": "Arm C - Agent Council",
}
ARM_NOTES = {
    "A": "One generation, rendered as produced. No retrieval, verification, or repair.",
    "B": "One generation, then AST checks, a sandboxed render, and search-and-replace repair.",
    "C": "The full council pipeline: Analyst, Architect, and Animator with the check and repair stages.",
}
TOPIC_ORDER = ["derivative", "backpropagation", "fourier", "doppler", "eigenvectors"]


def slug(topic: str) -> str:
    """Map a full topic string from index.csv onto its short slug."""
    lowered = topic.lower()
    for candidate in TOPIC_ORDER:
        if lowered.startswith(candidate):
            return candidate
    raise ValueError(f"unrecognized topic: {topic!r}")

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ConceptCast benchmark artifacts</title>
<style>
  :root {{
    color-scheme: light dark;
    --bg: #ffffff; --fg: #1b1f24; --muted: #5b6672; --line: #d8dee6;
    --card: #f7f9fb; --accent: #1f6feb;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg: #0d1117; --fg: #e6edf3; --muted: #9198a1; --line: #30363d;
             --card: #161b22; --accent: #6cb6ff; }}
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; padding: 2rem 1.25rem 4rem; background: var(--bg); color: var(--fg);
         font: 15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
  main {{ max-width: 1180px; margin: 0 auto; }}
  h1 {{ font-size: 1.6rem; margin: 0 0 .35rem; }}
  p.lead {{ color: var(--muted); margin: 0 0 1.5rem; max-width: 70ch; }}
  a {{ color: var(--accent); }}
  .controls {{ display: flex; flex-wrap: wrap; gap: .6rem; align-items: center;
               padding: .85rem 0 1.25rem; border-bottom: 1px solid var(--line); margin-bottom: 1.5rem; }}
  input[type=search] {{ flex: 1 1 260px; max-width: 380px; padding: .5rem .7rem; font: inherit;
                        color: var(--fg); background: var(--card);
                        border: 1px solid var(--line); border-radius: 6px; }}
  .count {{ color: var(--muted); font-variant-numeric: tabular-nums; }}
  h2 {{ font-size: 1.15rem; margin: 2.25rem 0 .2rem; }}
  h2:first-of-type {{ margin-top: 0; }}
  .armnote {{ color: var(--muted); margin: 0 0 .4rem; max-width: 78ch; }}
  h3 {{ font-size: .82rem; text-transform: uppercase; letter-spacing: .06em;
        color: var(--muted); margin: 1.5rem 0 .6rem; }}
  .grid {{ display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }}
  .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 8px;
           padding: .7rem; display: flex; flex-direction: column; gap: .55rem; }}
  video {{ width: 100%; aspect-ratio: 16 / 9; background: #000; border-radius: 5px; display: block; }}
  .name {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .78rem;
           word-break: break-all; }}
  .links {{ display: flex; gap: .9rem; flex-wrap: wrap; font-size: .84rem; }}
  .meta {{ color: var(--muted); font-size: .8rem; }}
  .hidden {{ display: none; }}
  footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--line);
            color: var(--muted); font-size: .85rem; }}
</style>
</head>
<body>
<main>
  <h1>ConceptCast benchmark artifacts</h1>
  <p class="lead">Every job that produced a video, grouped by arm and topic. Each card plays
  the rendered video beside a link to the Manim script that generated it. GitHub's file view
  cannot play these videos, which is why this page exists; the files themselves live under
  <a href="artifacts/">artifacts/</a>, one folder per job, and the bulk archives are on the
  <a href="https://github.com/{repo}/releases/tag/artifacts-v1">artifacts-v1 release</a>.</p>

  <div class="controls">
    <input type="search" id="filter" placeholder="Filter by topic, model, arm, or job number" aria-label="Filter jobs">
    <span class="count" id="count"></span>
  </div>

  <div id="cards">
{cards}
  </div>

  <footer>
    Players are lazy: nothing downloads until you press play. All {total} videos together
    are about 184 MB.
  </footer>
</main>
<script>
  const input = document.getElementById('filter');
  const cards = Array.from(document.querySelectorAll('.card'));
  const count = document.getElementById('count');
  const heads = Array.from(document.querySelectorAll('[data-head]'));
  const armHeads = Array.from(document.querySelectorAll('[data-arm-head]'));
  function apply() {{
    const q = input.value.trim().toLowerCase();
    let shown = 0;
    for (const c of cards) {{
      const hit = !q || c.dataset.key.includes(q);
      c.classList.toggle('hidden', !hit);
      if (hit) shown++;
    }}
    for (const h of heads) {{
      const group = h.dataset.head;
      const any = cards.some(c => c.dataset.group === group && !c.classList.contains('hidden'));
      h.classList.toggle('hidden', !any);
      const sect = h.nextElementSibling;
      if (sect && sect.classList.contains('grid')) sect.classList.toggle('hidden', !any);
    }}
    for (const h of armHeads) {{
      const arm = h.dataset.armHead;
      const any = cards.some(c => c.dataset.arm === arm && !c.classList.contains('hidden'));
      h.classList.toggle('hidden', !any);
    }}
    count.textContent = shown === cards.length
      ? `${{cards.length}} jobs`
      : `${{shown}} of ${{cards.length}} jobs`;
  }}
  input.addEventListener('input', apply);
  apply();
</script>
</body>
</html>
"""

CARD = """    <article class="card" data-key="{key}" data-group="{group}" data-arm="{arm}">
      <video controls preload="none" src="{video}"></video>
      <div class="name">{job}</div>
      <div class="meta">{topic} &middot; {model} &middot; rep {rep} &middot; job {seq}</div>
      <div class="links">
        <a href="{script}">scene.py</a>
        <a href="{folder}">job folder</a>
        <a href="{video}">video.mp4</a>
      </div>
    </article>
"""


def main() -> None:
    with (ARTIFACTS / "index.csv").open(newline="") as f:
        rows = [r for r in csv.DictReader(f) if r.get("code_file")]

    repo = "jdluu/ConceptCast-results"
    sections: list[str] = []
    for arm in sorted({r["arm"] for r in rows}):
        arm_rows = [r for r in rows if r["arm"] == arm]
        sections.append(f'  <h2 data-arm-head="arm_{arm}">{ARM_TITLES[arm]}</h2>')
        sections.append(f'  <p class="armnote" data-arm-head="arm_{arm}">{ARM_NOTES[arm]} '
                        f'{len(arm_rows)} of the jobs in this arm produced a video.</p>')
        topics = [t for t in TOPIC_ORDER if any(slug(r["topic"]) == t for r in arm_rows)]
        for topic in topics:
            group = f"arm_{arm}_{topic}"
            cards = [r for r in arm_rows if slug(r["topic"]) == topic]
            sections.append(f'  <h3 data-head="{group}">{topic} '
                            f'<span class="count">({len(cards)})</span></h3>')
            sections.append('  <div class="grid">')
            for r in cards:
                folder = str(pathlib.PurePosixPath(r["code_file"]).parent)
                job = folder.split("/")[-1]
                sections.append(CARD.format(
                    key=" ".join([job, f"arm {arm}", f"arm{arm}", r["topic"]]).lower(),
                    group=group,
                    arm=f"arm_{arm}",
                    video=html.escape(f"artifacts/{r['video']}"),
                    script=html.escape(f"artifacts/{r['code_file']}"),
                    folder=html.escape(f"artifacts/{folder}"),
                    job=html.escape(job),
                    topic=html.escape(r["topic"]),
                    model=html.escape(r["model"].split("/")[-1]),
                    rep=html.escape(r["rep"]),
                    seq=html.escape(r["job_seq"]),
                ))
            sections.append('  </div>')

    out = ROOT / "index.html"
    out.write_text(PAGE.format(cards="\n".join(sections), total=len(rows), repo=repo))
    print(f"wrote {out.relative_to(ROOT)}  ({out.stat().st_size:,} bytes, {len(rows)} jobs)")


if __name__ == "__main__":
    main()
