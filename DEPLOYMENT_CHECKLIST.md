# Digital Ocean Deployment Checklist

**Droplet:** 165.232.54.109  
**User:** root (SSH access) / girish (sudo user)  
**Application:** light-octo (NLP Graph Builder with Auth & AI)

---

## Pre-Deployment

- [ ] SSH to droplet: `ssh root@165.232.54.109`
- [ ] Run backups (see BACKUP_PLAN.md)
- [ ] Update system: `sudo apt update && sudo apt upgrade -y`
- [ ] Verify existing services: `sudo systemctl list-units --type=service`

---

## Step 1: System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx git

# Create application user
sudo useradd -m -d /home/nlp-app -s /bin/bash nlp-app
sudo usermod -aG www-data nlp-app
```

**Checklist:**
- [ ] Dependencies installed
- [ ] nlp-app user created
- [ ] nlp-app added to www-data group

---

## Step 2: Application Setup

```bash
# Clone light-octo repository
sudo -u nlp-app git clone https://github.com/gpad1234/light-octo.git /home/nlp-app/light-octo
cd /home/nlp-app/light-octo

# Create virtual environment
sudo -u nlp-app python3 -m venv venv

# Install dependencies
sudo -u nlp-app venv/bin/pip install --upgrade pip
sudo -u nlp-app venv/bin/pip install -r requirements.txt

# Setup environment file
sudo -u nlp-app cp .env.example .env
sudo nano /home/nlp-app/light-octo/.env
# Edit and add:
#   - OPENAI_API_KEY (if using AI features)
#   - SECRET_KEY (generate: python3 -c "import secrets; print(secrets.token_hex(32))")
#   - FLASK_ENV=production
#   - DEBUG=false
```

**Checklist:**
- [ ] Repository cloned to /home/nlp-app/light-octo
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured with SECRET_KEY
- [ ] OPENAI_API_KEY added (if needed)

---

## Step 3: Configure Gunicorn

```bash
# The gunicorn_config.py is already in the repo
# Verify it exists
ls -l /home/nlp-app/light-octo/gunicorn_config.py

# Test Gunicorn startup
cd /home/nlp-app/light-octo
sudo -u nlp-app venv/bin/gunicorn --config gunicorn_config.py app:app

# Press Ctrl+C to stop
```

**Checklist:**
- [ ] gunicorn_config.py present
- [ ] Gunicorn starts successfully
- [ ] Can access http://localhost:8000/health

---

## Step 4: Setup Systemd Service

```bash
# Copy service file
sudo cp /home/nlp-app/light-octo/nlp-graph-builder.service /etc/systemd/system/

# Edit service file with correct paths
sudo nano /etc/systemd/system/nlp-graph-builder.service
# Verify paths:
#   - WorkingDirectory=/home/nlp-app/light-octo
#   - ExecStart=/home/nlp-app/light-octo/venv/bin/gunicorn ...
#   - User=nlp-app
#   - Group=www-data

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl enable nlp-graph-builder
sudo systemctl start nlp-graph-builder

# Check status
sudo systemctl status nlp-graph-builder
```

**Checklist:**
- [ ] Service file copied
- [ ] Paths verified in service file
- [ ] Systemd daemon reloaded
- [ ] Service enabled for auto-start
- [ ] Service started successfully

---

## Step 5: Configure Nginx

```bash
# Copy nginx configuration
sudo cp /home/nlp-app/light-octo/nginx.conf /etc/nginx/sites-available/nlp-graph-builder

# Edit nginx config
sudo nano /etc/nginx/sites-available/nlp-graph-builder
# Update:
#   - server_name yourdomain.com; (or IP address for now: 165.232.54.109)
#   - ssl_certificate and ssl_certificate_key paths
#   - proxy_pass http://127.0.0.1:8000;

# Enable site
sudo ln -s /etc/nginx/sites-available/nlp-graph-builder /etc/nginx/sites-enabled/

# Disable default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

**Checklist:**
- [ ] Nginx config copied
- [ ] Domain/IP configured
- [ ] SSL paths updated (or skip for now)
- [ ] Site enabled
- [ ] Nginx test passed
- [ ] Nginx reloaded

---

## Step 6: SSL Certificate Setup (Optional - Skip for IP only)

```bash
# If using domain name only:
sudo certbot certonly --webroot -w /var/www/certbot -d yourdomain.com -d www.yourdomain.com

# Verify certificate
sudo ls -la /etc/letsencrypt/live/yourdomain.com/

# Update nginx config with cert paths
sudo nano /etc/nginx/sites-available/nlp-graph-builder
# Set:
#   ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
#   ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

# Test and reload
sudo nginx -t
sudo systemctl reload nginx

# Setup auto-renewal
sudo certbot renew --dry-run
```

**Checklist:**
- [ ] Certificate obtained (skip if IP-only)
- [ ] Certificate paths set in nginx
- [ ] Nginx test passed
- [ ] Auto-renewal tested

---

## Step 7: Verification

```bash
# Check application health
curl http://127.0.0.1:8000/health
# Should return: {"status":"healthy"}

# Check through nginx
curl http://localhost/health
# or with domain: curl https://yourdomain.com/health

# Check service status
sudo systemctl status nlp-graph-builder

# View logs
sudo journalctl -u nlp-graph-builder -f
tail -f /var/log/nginx/nlp-graph-builder_error.log
tail -f /var/log/nginx/nlp-graph-builder_access.log
```

**Checklist:**
- [ ] Health endpoint responds via Gunicorn
- [ ] Health endpoint responds via Nginx
- [ ] Service status is active
- [ ] No errors in logs
- [ ] Can access login page

---

## Step 8: Post-Deployment

```bash
# Check disk usage
df -h

# Check memory
free -h

# Monitor service
sudo systemctl list-units --type=service | grep nlp

# Setup log rotation (optional)
sudo nano /etc/logrotate.d/nlp-graph-builder
# Add:
# /var/log/gunicorn/*.log {
#     daily
#     rotate 7
#     compress
#     delaycompress
# }
```

**Checklist:**
- [ ] Disk space verified
- [ ] Memory usage acceptable
- [ ] All services running
- [ ] Log rotation configured

---

## Troubleshooting

### Service won't start
```bash
sudo systemctl status nlp-graph-builder
sudo journalctl -u nlp-graph-builder -n 50
# Check file permissions: sudo ls -la /home/nlp-app/light-octo/
```

### Nginx error
```bash
sudo nginx -t
sudo systemctl status nginx
sudo tail -f /var/log/nginx/error.log
```

### Application errors
```bash
cd /home/nlp-app/light-octo
sudo -u nlp-app venv/bin/gunicorn --config gunicorn_config.py app:app
# Run in foreground to see errors
```

### Permission denied errors
```bash
# Fix permissions
sudo chown -R nlp-app:www-data /home/nlp-app/light-octo
sudo chmod -R 755 /home/nlp-app/light-octo
sudo chmod 644 /home/nlp-app/light-octo/.env
```

---

## Rollback Procedure

If deployment fails:

```bash
# Stop the service
sudo systemctl stop nlp-graph-builder

# Restore from backup
sudo tar -xzf /home/girish/nginx-backup-*.tar.gz -C /
sudo tar -xzf /home/girish/systemd-backup-*.tar.gz -C /
sudo tar -xzf /home/girish/app-backup-*.tar.gz -C /

# Restart services
sudo systemctl daemon-reload
sudo systemctl restart nginx
sudo systemctl restart nlp-graph-builder
```

---

## Service Management Commands

```bash
# Start/Stop/Restart
sudo systemctl start nlp-graph-builder
sudo systemctl stop nlp-graph-builder
sudo systemctl restart nlp-graph-builder

# Check status
sudo systemctl status nlp-graph-builder

# View logs
sudo journalctl -u nlp-graph-builder -f

# Enable/Disable auto-start
sudo systemctl enable nlp-graph-builder
sudo systemctl disable nlp-graph-builder
```

---

## Deployment Complete! ✅

Once all steps are checked:
1. Access your application at `http://165.232.54.109` (or your domain)
2. Login with: **user/user123** or **admin/admin123**
3. Admin can access the AI Query tab
4. Monitor logs: `sudo journalctl -u nlp-graph-builder -f`

**Contact:** For issues, check PRODUCTION_DEPLOYMENT.md for detailed troubleshooting.
