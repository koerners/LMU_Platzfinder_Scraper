# Renew letsencrypt certificates.

/opt/letsencrypt/letsencrypt-auto certonly --standalone --renew-by-default --email $1 --agree-tos --no-eff-email -d $2