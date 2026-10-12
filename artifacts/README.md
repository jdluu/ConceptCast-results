# Artifacts

The rendered outputs of the benchmark, one directory per arm and one directory per job.
Each job folder holds the generated Manim script together with the video rendered from
it, so a link to one folder gives a reader both the code and its result.

## Layout

    artifacts/
      index.csv                  all 253 recorded jobs, with the artifacts each produced
      arm_A/
        armA_derivative_kimi-k2.6_rep1_seq004/
          scene.py               the generated Manim script
          video.mp4              the video rendered from it
        ...                      36 job folders
        manifest.json            per-job record for the arm
      arm_B/                     same layout, 68 job folders
      arm_C/                     same layout, 53 job folders

## Naming

Each job folder is named for the job it records:

    arm<A|B|C>_<topic>_<model>_rep<1|2>_seq<NNN>/

- **`topic`** is the short form of one of the five benchmark topics:
  `derivative`, `backpropagation`, `fourier`, `doppler`, `eigenvectors`.
  `manifest/topics.json` holds the full topic strings and the prompts sent.
- **`model`** is the roster name without its provider prefix
  (`z-ai/glm-5.3` becomes `glm-5.3`). `manifest/model_metadata.json` lists the roster.
- **`rep`** is the repetition within a cell, 1 or 2.
- **`seq`** is the `job_seq` in `manifest/jobs.csv`.

Inside every job folder the two files are always `scene.py` and `video.mp4`. The folder
name carries the identity, so nothing is lost by the generic names within it. Names
contain no spaces and can be used directly in URLs.

## Paths in the metadata

Paths written in `index.csv` and in each arm's `manifest.json` are relative to this
`artifacts/` directory, for example
`arm_C/armC_derivative_glm-5.3_rep1_seq101/scene.py`.

## Counts

| Arm | Jobs in `manifest.json` | With code and video |
|-----|------------------------|---------------------|
| A (Monolithic) | 100 | 36 |
| B (Monolithic + Repair) | 100 | 68 |
| C (Agent Council) | 53 | 53 |

Arm A and B manifests record every job attempted, including failures that produced no
artifact; those records carry no artifact path. Arm C's manifest covers the jobs that
produced artifacts, because the council's run state is recorded in `data/conceptcast.db`.

## Bulk download

The archives are published as release assets rather than committed, so the repository
carries only the individual files:

https://github.com/jdluu/ConceptCast-results/releases/tag/artifacts-v1

| Asset | Contents |
|-------|----------|
| `arm_A_videos.tar.gz` | 36 videos |
| `arm_B_videos.tar.gz` | 68 videos |
| `arm_C_videos.tar.gz` | 53 videos |

Each archive is flat: one file per job, named `<job>.mp4`, with no folder structure. The
name inside the archive is the folder name in the repository, so a downloaded file can be
matched back to its job, and from there to the script inside that folder.

    tar xzf arm_C_videos.tar.gz -C some/dir

## What is not here

`traces/renders/` in the repository root holds raw per-scene render work directories.
They are transient and are not tracked, so they are absent from a clone. Every video that
matters is under `artifacts/`.
