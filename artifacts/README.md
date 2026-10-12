# Artifacts

The rendered outputs of the benchmark, one directory per arm. Every file is named so
that the model, topic, and repetition are readable from the filename alone.

## Layout

    artifacts/
      index.csv            all 253 recorded jobs, with the artifact names each produced
      arm_A/
        code/              36 generated Manim scripts
        videos/            36 rendered videos, one per script
        manifest.json      per-job record for the arm
      arm_B/               same layout, 68 videos
      arm_C/               same layout, 53 videos

## Naming

    arm<A|B|C>_<topic>_<model>_rep<1|2>_seq<NNN>.<py|mp4>

Example: `armC_derivative_glm-5.3_rep1_seq101.py` pairs with
`armC_derivative_glm-5.3_rep1_seq101.mp4`.

- **`topic`** is the short form of one of the five benchmark topics:
  `derivative`, `backpropagation`, `fourier`, `doppler`, `eigenvectors`.
  `manifest/topics.json` holds the full topic strings and the prompts sent.
- **`model`** is the roster name without its provider prefix
  (`z-ai/glm-5.3` becomes `glm-5.3`). `manifest/model_metadata.json` lists the roster.
- **`rep`** is the repetition within a cell, 1 or 2.
- **`seq`** is the `job_seq` in `manifest/jobs.csv`. Code and video share it, so a
  script and its video always match by name.

Names contain no spaces, so they can be used directly in URLs.

## Counts

| Arm | Jobs in `manifest.json` | With code and video |
|-----|------------------------|---------------------|
| A (Monolithic) | 100 | 36 |
| B (Monolithic + Repair) | 100 | 68 |
| C (Agent Council) | 53 | 53 |

Arm A and B manifests record every job attempted, including failures that produced no
artifact. Arm C's manifest covers the jobs that produced artifacts, because the council's
run state is recorded in `data/conceptcast.db`.

## Bulk download

The archives are published as release assets rather than committed, so the repository
carries only the individual files:

https://github.com/jdluu/ConceptCast-results/releases/tag/artifacts-v1

| Asset | Contents |
|-------|----------|
| `arm_A_videos.tar.gz` | 36 videos |
| `arm_B_videos.tar.gz` | 68 videos |
| `arm_C_videos.tar.gz` | 53 videos |

Each archive holds the same filenames as its `videos/` directory, with no path prefix, so
a bulk download carries identical names to an individual one.

    tar xzf arm_C_videos.tar.gz -C some/dir

## What is not here

`traces/renders/` in the repository root holds raw per-scene render work directories.
They are transient and are not tracked, so they are absent from a clone. Every video that
matters is under `artifacts/`.
