# Backup Plan for Existing Nginx/Production Configuration

## Digital Ocean Droplet: 165.232.54.109

### Current Setup
- Root user with SSH access
- Sudo user: girish (no SSH access)
- Existing nginx configuration that needs backup

### Backup Strategy

#### 1. Backup Existing Nginx Configuration
```bash
# On the droplet, backup current nginx config
sudo tar -czf /home/girish/nginx-backup-$(date +%Y%m%d-%H%M%S).tar.gz /etc/nginx/
sudo chown girish:girish /home/girish/nginx-backup-*.tar.gz
```

#### 2. Backup Systemd Service Files
```bash
# Backup any existing systemd services
sudo tar -czf /home/girish/systemd-backup-$(date +%Y%m%d-%H%M%S).tar.gz /etc/systemd/system/
sudo chown girish:girish /home/girish/systemd-backup-*.tar.gz
```

#### 3. Backup Application Directory (if exists)
```bash
# If there's an existing app directory
sudo tar -czf /home/girish/app-backup-$(date +%Y%m%d-%H%M%S).tar.gz /home/nlp-app/ 2>/dev/null || true
sudo chown girish:girish /home/girish/app-backup-*.tar.gz
```

#### 4. Download Backups to Local Machine
```bash
# From local machine
scp root@165.232.54.109:/home/girish/nginx-backup-*.tar.gz ~/backups/
scp root@165.232.54.109:/home/girish/systemd-backup-*.tar.gz ~/backups/
scp root@165.232.54.109:/home/girish/app-backup-*.tar.gz ~/backups/
```

### Restore Procedure (if needed)
```bash
# On droplet, restore nginx config
sudo tar -xzf /home/girish/nginx-backup-*.tar.gz -C /
sudo systemctl restart nginx
```

### SSH Access Setup
Since only root has SSH access:
1. All deployment commands run via: `ssh root@165.232.54.109`
2. Use `sudo -u girish` for operations under girish user
3. Configure sudo passwordless for girish where needed

### Next Steps
1. SSH to droplet and run backup commands
2. Download backups to local machine
3. Proceed with light-octo deployment
4. Keep backups for rollback capability
