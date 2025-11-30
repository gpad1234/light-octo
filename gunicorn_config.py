"""
Gunicorn configuration for production deployment
"""
import os
import multiprocessing

# Server socket
bind = os.getenv('GUNICORN_BIND', '127.0.0.1:8000')
backlog = 2048

# Worker processes
workers = os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1)
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = os.getenv('GUNICORN_ACCESS_LOG', '/var/log/gunicorn/access.log')
errorlog = os.getenv('GUNICORN_ERROR_LOG', '/var/log/gunicorn/error.log')
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'nlp-graph-builder'

# Server mechanics
daemon = False
pidfile = os.getenv('GUNICORN_PIDFILE', '/var/run/gunicorn/nlp-graph-builder.pid')
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
ca_certs = None
suppress_ragged_eof = True

# Application
raw_env = []
preload_app = False
forwarded_allow_ips = os.getenv('GUNICORN_FORWARDED_ALLOW_IPS', '127.0.0.1')
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on',
}
