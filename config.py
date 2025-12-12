# config.py
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env if present (for secrets)
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Monitoring interval (seconds)
INTERVAL = int(os.getenv("MONITOR_INTERVAL", "30"))  # default 30s

# Thresholds (percentages)
CPU_THRESHOLD_PERCENT = int(os.getenv("CPU_THRESHOLD_PERCENT", "85"))
MEM_THRESHOLD_PERCENT = int(os.getenv("MEM_THRESHOLD_PERCENT", "85"))
DISK_THRESHOLD_PERCENT = int(os.getenv("DISK_THRESHOLD_PERCENT", "90"))

# Disk to check (e.g. "/" on Linux)
DISK_PARTITION = os.getenv("DISK_PARTITION", "/")

# Top N processes to include in alert
TOP_N_PROCESSES = int(os.getenv("TOP_N_PROCESSES", "5"))

# Alerting: email config (optional)
SMTP_ENABLED = os.getenv("SMTP_ENABLED", "false").lower() in ("1","true","yes")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "alerts@example.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
SMTP_TO = [s.strip() for s in os.getenv("SMTP_TO", "admin@example.com").split(",") if s.strip()]

# Alerting: webhook (optional) e.g., Slack / Teams / custom
WEBHOOK_ENABLED = os.getenv("WEBHOOK_ENABLED", "false").lower() in ("1","true","yes")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

# Logging settings
LOG_FILE = os.getenv("LOG_FILE", str(Path(__file__).parent / "system-health-monitor.log"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Misc
HOSTNAME = os.getenv("HOSTNAME", os.uname().nodename if hasattr(os, "uname") else "unknown-host")
