# The World in One Day — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/syuaibcvk/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/syuaibcvk/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for the make.fun bounty
[news-image-20261125](https://make.fun/bounty/news-image-20261125)
— "Sum up 25 November's world news in one image" ($100 USDC escrowed,
50 places).

## What the image shows

A one-page newspaper front page, "The World in One Day — Wednesday
25 November 2026" (No. 25), drawn from scratch with Pillow:

- **Lead — Ukraine / Russia oil war:** President Putin vows
  "inevitable" retaliation after Ukraine kept striking Russian
  refineries despite a direct request from US President Trump to stop;
  overnight, Ukrainian drones hit two major refineries in the Samara
  region (Syzran and Kuibyshev), with Russian crude runs down about
  45% since late October. A Russian strike on flats in Zaporizhzhia
  killed 2 people and wounded about 50.
- **Markets:** Monday's rally dies in a day — Nasdaq −1.48%, S&P 500
  −0.50%, chip stocks down nearly 8%; Bitcoin slips back under
  $60,000 (~$59,300) as spot Bitcoin ETFs see $569.7m of outflows on
  23 November, a fifth straight day.
- **Riyadh:** a Houthi drone hits the 385-metre PIF Tower again;
  11 wounded, at least 2 critical — the second hit in under a week.
- **China:** a Brooklyn jury convicts Huawei of conspiracy to steal
  trade secrets and bank fraud; China hands a death sentence in an
  espionage case; Shanghai party chief Chen Jining is under
  investigation.
- **Gaza:** an Israeli strike kills Hamas internal security chief
  Naim Abu Nahl among 7 people.
- **In Brief:** Sarkozy and Carla Bruni ordered to stand trial;
  Indonesia's vice-president resigns; US prepares fresh tariff hikes
  on China and the EU; CIA and ODNI hit by a hack of unclassified
  systems; Norway to give Ukraine at least $7bn in 2027; Mount Mayon
  eruption in the Philippines.

Sources are listed in the footer: Reuters, AP, The Independent, The
Wall Street Journal, Al Jazeera, Kyiv Independent, Dawn, KuCoin,
Finnhub.

## How to build

Requires Python 3.13 (3.12 works locally) and Pillow, plus the DejaVu
fonts shipped with most Linux systems
(`/usr/share/fonts/truetype/dejavu/`). No network, no clock, no
randomness — the program draws fixed text with fixed geometry, so
every run writes byte-identical output.

```sh
python3 main.py
# writes ./entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)

# verify a rendered file against the pinned SHA-256:
python3 main.py --verify entry.png
```

`main.py` embeds a SHA-256 pin of the image it produces and exits 1
if the rendered bytes do not match it (a single flipped pixel fails
verification). Two runs to different directories produce identical
bytes.

## License

MIT — see [LICENSE](LICENSE).
