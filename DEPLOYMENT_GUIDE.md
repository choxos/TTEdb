# TTEdb VPS Deployment Guide

This guide provides step-by-step instructions for deploying TTEdb to a VPS at `ttedb.xeradb.com`.

## Prerequisites

- VPS with Ubuntu 20.04 or later
- PostgreSQL database `ttedb_production` with user `ttedb_user`
- Domain configured: `ttedb.xeradb.com`
- SSL certificate (Let's Encrypt recommended)

## 1. Server Setup

### Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Install Required Packages
```bash
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib supervisor git
```

### Install Node.js (for frontend assets)
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

## 2. Database Setup

### Configure PostgreSQL
```bash
sudo -u postgres psql
```

```sql
-- Create database and user
CREATE DATABASE ttedb_production;
CREATE USER ttedb_user WITH ENCRYPTED PASSWORD 'your_secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ttedb_production TO ttedb_user;
ALTER USER ttedb_user CREATEDB;

-- Exit psql
\q
```

### Configure PostgreSQL for Django
```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

Add this line:
```
local   ttedb_production    ttedb_user                              md5
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

## 3. Project Deployment

### Create Application Directory
```bash
sudo mkdir -p /var/www/html/ttedb
sudo chown $USER:$USER /var/www/html/ttedb
cd /var/www/html/ttedb
```

### Clone Repository
```bash
git clone https://github.com/your-username/TTEdb.git .
```

### Create Virtual Environment
```bash
python3 -m venv ttedb_env
source ttedb_env/bin/activate
```

### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Create Environment File
```bash
nano .env
```

Add production configuration:
```env
DEBUG=False
SECRET_KEY=your_very_secure_secret_key_here_change_this
DATABASE_NAME=ttedb_production
DATABASE_USER=ttedb_user
DATABASE_PASSWORD=your_secure_password_here
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=ttedb.xeradb.com,localhost,127.0.0.1
XERA_DB_SHARED_THEME_PATH=/var/www/html/xeradb/shared_theme
```

### Run Migrations
```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

### Import Data
```bash
python manage.py import_tte_data --clear-existing
```

### Create Superuser
```bash
python manage.py createsuperuser
```

## 4. Gunicorn Configuration

### Create Gunicorn Service File
```bash
sudo nano /etc/systemd/system/ttedb.service
```

```ini
[Unit]
Description=TTEdb Gunicorn daemon
Requires=ttedb.socket
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/var/www/html/ttedb
ExecStart=/var/www/html/ttedb/ttedb_env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --timeout 60 \
          --keep-alive 2 \
          --max-requests 1000 \
          --max-requests-jitter 100 \
          --bind unix:/run/gunicorn/ttedb.sock \
          ttedb_project.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Environment="PATH=/var/www/html/ttedb/ttedb_env/bin"
EnvironmentFile=/var/www/html/ttedb/.env

[Install]
WantedBy=multi-user.target
```

### Create Socket File
```bash
sudo nano /etc/systemd/system/ttedb.socket
```

```ini
[Unit]
Description=TTEdb gunicorn socket

[Socket]
ListenStream=/run/gunicorn/ttedb.sock
SocketUser=www-data
SocketMode=600

[Install]
WantedBy=sockets.target
```

### Set Permissions
```bash
sudo chown -R www-data:www-data /var/www/html/ttedb
sudo chmod -R 755 /var/www/html/ttedb
```

### Start Services
```bash
sudo systemctl daemon-reload
sudo systemctl start ttedb.socket
sudo systemctl enable ttedb.socket
sudo systemctl start ttedb.service
sudo systemctl enable ttedb.service
```

## 5. Nginx Configuration

### Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/ttedb
```

```nginx
server {
    listen 80;
    server_name ttedb.xeradb.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ttedb.xeradb.com;

    # SSL Configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/ttedb.xeradb.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ttedb.xeradb.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Security Headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/javascript application/xml+rss application/json;

    client_max_body_size 100M;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }

    location /static/ {
        alias /var/www/html/ttedb/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn/ttedb.sock;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn/ttedb.sock;
    }
}
```

### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/ttedb /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 6. SSL Certificate (Let's Encrypt)

### Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Obtain Certificate
```bash
sudo certbot --nginx -d ttedb.xeradb.com
```

### Auto-renewal
```bash
sudo crontab -e
```

Add this line:
```
0 12 * * * /usr/bin/certbot renew --quiet
```

## 7. Monitoring and Logs

### Setup Log Rotation
```bash
sudo nano /etc/logrotate.d/ttedb
```

```
/var/www/html/ttedb/ttedb.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload ttedb.service
    endscript
}
```

### Check Service Status
```bash
# Check TTEdb service
sudo systemctl status ttedb.service

# Check logs
sudo journalctl -u ttedb.service -f

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 8. Backup Strategy

### Database Backup Script
```bash
sudo nano /usr/local/bin/backup_ttedb.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/ttedb"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="ttedb_production"
DB_USER="ttedb_user"

mkdir -p $BACKUP_DIR

# Database backup
PGPASSWORD="your_password_here" pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/ttedb_db_$DATE.sql

# Code backup
tar -czf $BACKUP_DIR/ttedb_code_$DATE.tar.gz -C /var/www/html ttedb

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
sudo chmod +x /usr/local/bin/backup_ttedb.sh
```

### Schedule Backups
```bash
sudo crontab -e
```

Add:
```
0 2 * * * /usr/local/bin/backup_ttedb.sh >> /var/log/ttedb_backup.log 2>&1
```

## 9. Maintenance Commands

### Update Application
```bash
cd /var/www/html/ttedb
git pull origin main
source ttedb_env/bin/activate
pip install -r requirements.txt --upgrade
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart ttedb.service
```

### Import New Data
```bash
cd /var/www/html/ttedb
source ttedb_env/bin/activate
python manage.py import_tte_data
```

### Clear Cache (if implemented)
```bash
cd /var/www/html/ttedb
source ttedb_env/bin/activate
python manage.py clearcache
```

## 10. Security Checklist

- [ ] Firewall configured (UFW recommended)
- [ ] SSH key-based authentication
- [ ] Regular security updates
- [ ] Database password is strong and unique
- [ ] Django SECRET_KEY is secure and unique
- [ ] DEBUG=False in production
- [ ] SSL certificate installed and auto-renewal configured
- [ ] Regular backups scheduled
- [ ] Log monitoring setup
- [ ] Rate limiting configured
- [ ] Security headers configured

## Troubleshooting

### Common Issues

1. **Permission Errors**
   ```bash
   sudo chown -R www-data:www-data /var/www/html/ttedb
   sudo chmod -R 755 /var/www/html/ttedb
   ```

2. **Database Connection Issues**
   - Check PostgreSQL is running: `sudo systemctl status postgresql`
   - Verify credentials in `.env` file
   - Check `pg_hba.conf` configuration

3. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic --noinput
   sudo systemctl restart ttedb.service
   ```

4. **Service Won't Start**
   ```bash
   sudo journalctl -u ttedb.service -f
   ```

### Performance Optimization

1. **Enable Redis for Caching** (Optional)
   ```bash
   sudo apt install redis-server
   pip install django-redis
   ```

2. **Database Optimization**
   - Enable connection pooling
   - Configure PostgreSQL performance settings
   - Regular VACUUM and ANALYZE

3. **Monitoring**
   - Setup monitoring with tools like Prometheus/Grafana
   - Monitor disk space, memory usage, and response times

## Support

For issues related to deployment:
1. Check the logs first
2. Verify all services are running
3. Check the GitHub repository for updates
4. Contact the development team

---

**Important**: Remember to change all default passwords and keys before deploying to production! 