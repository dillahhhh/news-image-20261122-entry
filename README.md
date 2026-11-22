# World News — Sunday 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/dillahhhh/news-image-20261122-entry/rank.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/dillahhhh/news-image-20261122-entry/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image that sums up the world's news of Sunday 22 November 2026: a
dense newsroom dashboard in Bahasa Indonesia — a date-locked header, a
dotted world map with 6 numbered pins, a UTC strip with verified event
times, and 34 dated cards (1 lead + 5 secondary + 28 regular), one card
per story, each carrying an epistemic tag ([RESMI] / [KLAIM] / [DATA])
and its source. Lead story: COP31 collapses in Antalya with no deal
over fossil fuels. No fact, timestamp, outlet name, or number is
invented: every card traces to a story reported on 22 November 2026
(OneTurn day page + primary outlets; Saturday events are labelled as
reported on Sunday, and the strip marks them as such).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies the pre-rendered
`entry.png` (1024×1024, ≤ 1 MiB) to the output directory: same bytes on
every run, no randomness, no clock, no network. `build_image.py`
(Pillow + DejaVu fonts shipped in `fonts/`) renders `entry.png`
deterministically from `stories.py`.

## Bounty

Entered in [Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122) on make.fun.

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261122).</sub>
