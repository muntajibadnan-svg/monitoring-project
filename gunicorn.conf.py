"""Gunicorn production configuration."""

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5000"

# Worker processes
# Recommendation: 2 * num_cores + 1
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
worker_tmp_dir = "/dev/shm"  # Use RAM for heartbeat (avoids disk I/O issues in containers)

# Timeouts
timeout = 30
graceful_timeout = 30
keepalive = 5

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = os.getenv("LOG_LEVEL", "info")

# Security
limit_request_line = 8190
limit_request_fields = 100

# Server mechanics
preload_app = True
max_requests = 1000         # Restart workers after N requests (prevents memory leaks)
max_requests_jitter = 50    # Random jitter to avoid all workers restarting at once
