# LMU Platzfinder Scraper
- Schreibt alle 15 Minuten die Auslastung der LMU Bibliotheken in eine Datenbank 
- Stellt die Daten als JSON, sowie mehrere Grafiken als SVG-Strings über eine API-Schnittstelle bereit
- Verschlüsselung mit HTTPS unter Verwendung eines NGINX Reverse Proxys und automatischer Verwendung von Let's Encrypt Zertifikaten

### [Angular Frontend](https://github.com/koerners/Platzfinder)


### Setup:
#### On a webserver with DNS-records pointing to a valid domain:

1. Install Docker & Docker-Compose

2. Change VIRTUAL_HOST, LETSENCRYPT_HOST and LETSENCRYPT_EMAIL in /LMU_Platzfinder_Scraper/docker-compose.yaml
3. Run in /LMU_Platzfinder_Scraper/ngnix/: 
```
(sudo) docker-compose up -d 
```
4. Run in /LMU_Platzfinder_Scraper:
```
(sudo) docker-compose up -d 
```
5. Setup Crontab
```
*/15 * * * * docker start {ID of scraper container}  >> ~/cron.log 2>&1
```

