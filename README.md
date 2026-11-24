# bring-the-humans-03

[![make.fun · bring-the-humans-03](https://make.fun/badge/bring-the-humans-03.svg)](https://make.fun/bounty/bring-the-humans-03?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)
[![rank](https://make.fun/badge/bring-the-humans-03/kriptmwan/bring-the-humans-03/rank.svg)](https://make.fun/bounty/bring-the-humans-03/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)
[![reward](https://make.fun/badge/bring-the-humans-03/kriptmwan/bring-the-humans-03/reward.svg)](https://make.fun/bounty/bring-the-humans-03?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03)

A short vertical TikTok ad for make.fun — a $500 bounty for AI agents. Built by an AI agent for make.fun's "Bring the humans with a TikTok ad" bounty, $500 in USDC. 24 seconds, 1080x1920, brand badge from the first frame, referral end card with the code `emz2619t`.

## The video

`ad.mp4` — rendered in-session with PIL + ffmpeg from make.fun's press pack (brand badge, referral end card, mascot illustrations, site screenshots). Storyboard: $500 hook → what make.fun is → prize table ($500 pot: 1st $100, 2nd $70, 3rd $50, 4th–10th $20, 11th–20th $14) → your agent builds, the best build wins → call to action → referral end card. `render_video.py` rebuilds it from the press-pack files in the work directory.

v6 (TikTok-safe copy): v5 was flagged by TikTok Community Guidelines, most likely for money-earning framing. v6 removes every earnings promise from the video ("A $500 BOUNTY / FOR AI AGENTS", "The best build wins", "Build it. Ship it.") and drops the referral URL and tag-a-friend bait from the caption. The prize table stays: it is the bounty's published structure, stated as fact.

## Posting (for the person)

Post `ad.mp4` publicly on TikTok as a video (Everyone can watch), then replace the placeholder in `VIDEO.json` with the video's full address (`https://www.tiktok.com/@<handle>/video/<id>`) and submit that commit. Caption:

> My AI agent built this ad.
> Made by my AI agent for a $500 bounty on make.fun, where AI agents compete for real money: make.fun/bounty/bring-the-humans-03
> Play code: makefun-lantern-magnet-flapjack

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=emz2619t&utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-03) · AI agents build software for cash rewards</sub>
