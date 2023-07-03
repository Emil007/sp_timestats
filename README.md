# sp_timestats
A bunch of scripts i cubbled together with big help from chatgpt - pulls als pokemon from rdm db, analyzes their time between seen and despawn time (for now) and writes that to DB for grafana


**pullstats.py** - pulls all pokemon from db and saves them locally to pkmn.db. Marks as pokemon pulled as checked (needs column "checked" in pokemon table)

**analyze.py** - analyzes time between despawn and first_seen, writes findings to stats.db and moves analyzed entries to archive.db

**sendstats.py** - sends stats to database, needs table timestats:

**stats.py** - runs all of them in order for cronjob
```
CREATE TABLE IF NOT EXISTS `timestats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL DEFAULT current_timestamp(),
  `s59` int(11), `s58` int(11), `s57` int(11), `s56` int(11), `s55` int(11), `s54` int(11), `s53` int(11), `s52` int(11), `s51` int(11),
  `s50` int(11), `s49` int(11), `s48` int(11), `s47` int(11), `s46` int(11), `s45` int(11), `s44` int(11), `s43` int(11), `s42` int(11), `s41` int(11),
  `s40` int(11), `s39` int(11), `s38` int(11), `s37` int(11), `s36` int(11), `s35` int(11), `s34` int(11), `s33` int(11), `s32` int(11), `s31` int(11),
  `s30` int(11), `s29` int(11), `s28` int(11), `s27` int(11), `s26` int(11), `s25` int(11), `s24` int(11), `s23` int(11), `s22` int(11), `s21` int(11),
  `s20` int(11), `s19` int(11), `s18` int(11), `s17` int(11), `s16` int(11), `s15` int(11), `s14` int(11), `s13` int(11), `s12` int(11), `s11` int(11),
  `s10` int(11), `s9` int(11), `s8` int(11), `s7` int(11), `s6` int(11), `s5` int(11), `s4` int(11), `s3` int(11), `s2` int(11), `s1` int(11), `s0` int(11),
  PRIMARY KEY (`id`)
);
```

can then be used in grafana with something like

```
SELECT
    time,
    ROUND(((s29 + s28 + s27 + s26) / (s29 + s28 + s27 + s26 + s25 + s24 + s23 + s22 + s21 + s20 + s19 + s18 + s17 + s16 + s15 + s14 + s13 + s12 + s11 + s10 + s9 + s8 + s7 + s6 + s5 + s4 + s3 + s2 + s1 + s0)) * 100, 2) AS "OK",
    ROUND(((s25 + s24 + s23 + s22 + s21 + s20) / (s29 + s28 + s27 + s26 + s25 + s24 + s23 + s22 + s21 + s20 + s19 + s18 + s17 + s16 + s15 + s14 + s13 + s12 + s11 + s10 + s9 + s8 + s7 + s6 + s5 + s4 + s3 + s2 + s1 + s0)) * 100, 2) AS "pass",
    ROUND(((s19 + s18 + s17 + s16 + s15 + s14 + s13 + s12 + s11 + s10) / (s29 + s28 + s27 + s26 + s25 + s24 + s23 + s22 + s21 + s20 + s19 + s18 + s17 + s16 + s15 + s14 + s13 + s12 + s11 + s10 + s9 + s8 + s7 + s6 + s5 + s4 + s3 + s2 + s1 + s0)) * 100, 2) AS "bad",
    ROUND(((s9 + s8 + s7 + s6 + s5 + s4 + s3 + s2 + s1 + s0) / (s29 + s28 + s27 + s26 + s25 + s24 + s23 + s22 + s21 + s20 + s19 + s18 + s17 + s16 + s15 + s14 + s13 + s12 + s11 + s10 + s9 + s8 + s7 + s6 + s5 + s4 + s3 + s2 + s1 + s0)) * 100, 2) AS "fail"
FROM timestats
