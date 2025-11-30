# Production Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying the NLP Graph Builder application to production using **Nginx** as a reverse proxy and **Gunicorn** as the application server on an Ubuntu/Debian Linux system.

## Architecture
```
Client (HTTPS)
    ↓
Nginx (Port 443) - Reverse Proxy, SSL, Static Files
    ↓
Gunicorn (Port 8000) - WSGI Application Server
    ↓
Flask Application
```

## Prerequisites
- Ubuntu 20.04+ or Debian 10+
- Python 3.8+
- Nginx
- Systemd (for service management)
- SSL Certificate (Let's Encrypt recommended)
- Sudo access

## Deployment Steps

### 1. System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx

# Create application user
sudo useradd -m -d /home/nlp-app -s /bin/bash nlp-app
sudo usermod -aG www-data nlp-app
```

### 2. Application Setup

```bash
# Clone repository
sudo -u nlp-app git clone https://github.com/gpad1234/fuzzy-adventure.git /home/nlp-app/fuzzy-adventure
cd /home/nlp-app/fuzzy-adventure

# Switch to prod branch
sudo -u nlp-app git checkout prod

# Create virtual environment
sudo -u nlp-app python3 -m venv /home/nlp-app/fuzzy-adventure/.venv

# Install dependencies
sudo -u nlp-app /home/nlp-app/fuzzy-adventure/.venv/bin/pip install --upgrade pip setuptools wheel
sudo -u nlp-app /home/nlp-app/fuzzy-adventure/.venv/bin/pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Create .env file from example
sudo -u nlp-app cp .env.example /home/nlp-app/fuzzy-adventure/.env

# Edit .env with your settings
sudo nano /home/nlp-app/fuzzy-adventure/.env
```

**Important settings to configure:**
- `SECRET_KEY` - Generate a strong secret key: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- `OPENAI_API_KEY` - Your OpenAI API key
- `GUNICORN_WORKERS` - Set based on CPU cores: `(CPU_CORES * 2) + 1`

### 4. Create Log Directories

```bash
# Create log directories
sudo mkdir -p /var/log/gunicorn /var/run/gunicorn
sudo chown nlp-app:www-data /var/log/gunicorn /var/run/gunicorn
sudo chmod 775 /var/log/gunicorn /var/run/gunicorn
```

### 5. Setup Systemd Service

```bash
# Copy service file
sudo cp /home/nlp-app/fuzzy-adventure/nlp-graph-builder.service /etc/systemd/system/

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable nlp-graph-builder
sudo systemctl start nlp-graph-builder

# Check status
sudo systemctl status nlp-graph-builder

# View logs
sudo journalctl -u nlp-graph-builder -f
```

### 5.1 Service Management Commands

Once the service is running, use these commands to manage it:

```bash
# Check service status
sudo systemctl status nlp-graph-builder

# Stop the service
sudo systemctl stop nlp-graph-builder

# Start the service
sudo systemctl start nlp-graph-builder

# Restart the service (useful for reloading config changes)
sudo systemctl restart nlp-graph-builder

# View real-time logs
sudo journalctl -u nlp-graph-builder -f

# View logs from the last hour
sudo journalctl -u nlp-graph-builder --since "1 hour ago"

# For manual/direct Gunicorn shutdown (if not using systemd)
pkill -f "gunicorn"
# or
kill <PID>  # Replace <PID> with process ID from: ps aux | grep gunicorn
```

### 6. Configure Nginx

```bash
# Copy nginx configuration
sudo cp /home/nlp-app/fuzzy-adventure/nginx.conf /etc/nginx/sites-available/nlp-graph-builder

# Edit nginx config with your domain
sudo nano /etc/nginx/sites-available/nlp-graph-builder
# Replace "yourdomain.com" with your actual domain

# Enable site
sudo ln -s /etc/nginx/sites-available/nlp-graph-builder /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 7. SSL Certificate Setup (Let's Encrypt)

```bash
# Obtain certificate
sudo certbot certonly --webroot -w /var/www/certbot -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run

# Auto-renewal is automatically configured
sudo systemctl enable certbot.timer
```

### 8. Firewall Configuration (UFW)

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

## Verification

```bash
# Check if Gunicorn is running
ps aux | grep gunicorn

# Test application endpoint
curl http://localhost:8000/health

# Check Nginx status
sudo systemctl status nginx

# View Nginx logs
sudo tail -f /var/log/nginx/nlp-graph-builder_access.log
sudo tail -f /var/log/nginx/nlp-graph-builder_error.log

# View Gunicorn logs
sudo journalctl -u nlp-graph-builder -n 50
```

## Management Commands

```bash
# Start/Stop/Restart application
sudo systemctl start nlp-graph-builder
sudo systemctl stop nlp-graph-builder
sudo systemctl restart nlp-graph-builder

# View application status
sudo systemctl status nlp-graph-builder

# View logs
sudo journalctl -u nlp-graph-builder -f

# Reload nginx without dropping connections
sudo systemctl reload nginx

# Update application
cd /home/nlp-app/fuzzy-adventure
sudo -u nlp-app git pull origin prod
sudo systemctl restart nlp-graph-builder
```

## Monitoring

### Health Check
```bash
curl https://yourdomain.com/health
```

Expected response:
```json
{"status":"healthy"}
```

### Check Log Files
```bash
# Application errors
sudo tail -f /var/log/gunicorn/nlp-app-error.log

# Access logs
sudo tail -f /var/log/gunicorn/nlp-app-access.log

# Nginx errors
sudo tail -f /var/log/nginx/nlp-graph-builder_error.log
```

## Performance Tuning

### Worker Count
Edit `/etc/systemd/system/nlp-graph-builder.service` or `.env`:
```bash
GUNICORN_WORKERS=8  # Adjust based on: (CPU cores × 2) + 1
```

### Connection Limits
In `/etc/nginx/sites-available/nlp-graph-builder`:
```nginx
worker_connections 1024;
keepalive_timeout 65;
```

### Session Storage
For production, consider using Redis or database for session storage instead of filesystem.

## Troubleshooting

### Application won't start
```bash
# Check for Python errors
cd /home/nlp-app/fuzzy-adventure
sudo -u nlp-app ./.venv/bin/python app.py

# Check logs
sudo journalctl -u nlp-graph-builder -n 100
```

### 502 Bad Gateway
- Check if Gunicorn is running: `sudo systemctl status nlp-graph-builder`
- Check socket: `sudo netstat -tln | grep 8000`
- Review Nginx error log: `sudo tail -f /var/log/nginx/nlp-graph-builder_error.log`

### Permission denied errors
```bash
# Fix permissions
sudo chown -R nlp-app:www-data /home/nlp-app/fuzzy-adventure
sudo chmod -R 755 /home/nlp-app/fuzzy-adventure
```

### SSL Certificate issues
```bash
# Check certificate status
sudo certbot certificates

# Renew manually
sudo certbot renew --force-renewal
```

## Security Considerations

1. **Secrets**: Store all secrets in `.env`, never commit them
2. **SSL**: Always use HTTPS in production
3. **Firewall**: Restrict access to only necessary ports
4. **Updates**: Keep system and dependencies up to date
5. **Backups**: Regular backups of `.env` and session data
6. **CORS**: Configure CORS appropriately for your needs
7. **Rate Limiting**: Consider adding rate limiting in Nginx for sensitive endpoints

## Backup Strategy

```bash
# Backup application
sudo tar -czf /backups/nlp-app-$(date +%Y%m%d).tar.gz /home/nlp-app/fuzzy-adventure

# Backup .env (secure storage)
sudo cp /home/nlp-app/fuzzy-adventure/.env /backups/.env.backup-$(date +%Y%m%d)
sudo chmod 600 /backups/.env.backup-*

# Restore
sudo tar -xzf /backups/nlp-app-YYYYMMDD.tar.gz -C /home/nlp-app/
```

## CI/CD Integration

For automated deployments via GitHub Actions:

```bash
# Set up SSH key for deployment
ssh-keygen -t ed25519 -f /home/nlp-app/.ssh/deploy_key

# Add public key to authorized_keys
cat /home/nlp-app/.ssh/deploy_key.pub >> /home/nlp-app/.ssh/authorized_keys

# Add private key as GitHub secret: DEPLOY_KEY
# Add host as GitHub secret: DEPLOY_HOST
```

## Support & Issues

- **GitHub Repository**: https://github.com/gpad1234/fuzzy-adventure
- **Issues**: Report bugs and feature requests on GitHub Issues
- **Documentation**: See README.md in repository root

---

**Last Updated**: November 26, 2025
