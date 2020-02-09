# LMU Platzfinder Scraper
Schreibt alle 15 Minuten die Auslastung der LMU Bibliotheken in eine Datenbank und stellt die Daten als JSON / Graphen über eine API-Schnittstelle bereit.

Crontab
```
*/15 * * * * $(which python3) /home/{username}/main.py  >> ~/cron.log 2>&1
```

[Frontend](https://github.com/koerners/Platzfinder)
