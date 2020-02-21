# Install lets encrypt certificates.

git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt
/opt/letsencrypt/letsencrypt-auto certonly --standalone --email contact@skoerner.com --agree-tos --no-eff-email -d api.platzfinder.com -d www.api.platzfinder.com