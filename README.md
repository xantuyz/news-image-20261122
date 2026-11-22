[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/xantuyz/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/xantuyz/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)


Entry for the make.fun bounty: https://make.fun/bounty/news-image-20261122


# The World Today — Sunday, 22 November 2026


One image summing up the world's news of 22 November 2026, drawn by
`render.py` (Python + PIL, build time only, no network, no external
assets) and shipped as `entry.png`; `main.py` (standard library only)
copies it into `/output/entry.png`.


## The six stories


1. **Lead — Baltic Sea:** Russian cargo ship Sparta II hit by two drones
   in the Gulf of Finland on Saturday 21 November, caught fire and drifted
   into Finnish waters; all 16 crew escaped in lifeboats. Finland says
   Ukraine was most likely behind the attack.
2. **Mexico:** Top-10 FBI fugitive Fausto Isidro Meza Flores ("Chapo
   Isidro") captured in Sinaloa on Friday night, 20 November; $5m US
   reward; 11 killed in follow-on violence.
3. **Climate — COP31, Antalya:** talks ran into Saturday with no mention
   of fossil fuels in the latest draft, despite about 130 nations demanding
   phase-out language; talks may run into Sunday.
4. **Ukraine:** "Triple-tap" Russian strike on Kryvyi Rih on Friday night,
   20 November — a 7-year-old and a 20-year-old paramedic killed, 60+
   hurt, on Ukraine's Children's Day.
5. **Peru:** Magnitude 6.7 earthquake on Friday 20 November at 19:09 local
   time near Carhuamayo, Junín, 108 km deep; felt in Lima; no casualties
   reported.
6. **United States:** FBI investigating a suspected hack of the National
   Crime Information Center (NCIC), its national crime database — the
   second intrusion into an FBI system in months.


Sources: Reuters, CNN, AP, USGS.


## Run


```
python3 main.py
```


Copies the shipped `entry.png` (1024x1024 PNG, under 1 MiB) to
`$MAKEFUN_OUTPUT_DIR` (or `/output`) and verifies its SHA-256.


## License


MIT — see `LICENSE`.

