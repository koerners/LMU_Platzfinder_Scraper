# LMU Platzfinder Scraper
Dokumentiert stündlich zwischen 8 und 24 Uhr die Auslastung der LMU Bibliotheken.

Für die Benachrichtigung:
```
notify-run register
```
Crontab
```
*/15 * * * * $(which python3) /home/{username}/main.py  >> ~/cron.log 2>&1
```
