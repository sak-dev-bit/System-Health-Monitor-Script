
# 📘 **System Health Monitor — README**

## 📌 Overview

**System Health Monitor** is a lightweight, automated monitoring tool that continuously tracks system resources such as CPU usage, memory consumption, disk utilization, and top processes.
It sends alerts via **Email** or **Webhook (Slack, Teams, etc.)** when resource thresholds are crossed.

This project is built using **Python + psutil**, with optional deployment via **systemd** or **Docker**, making it suitable for developers, sysadmins, and infrastructure monitoring.

---

# 🚀 Features

* ✔ **CPU, Memory, Disk Monitoring**
* ✔ **Top N processes included in every alert**
* ✔ **Email Alerts (SMTP)**
* ✔ **Webhook Alerts (Slack, Teams, Custom APIs)**
* ✔ **Configurable thresholds**
* ✔ **Environment-based configuration using `.env`**
* ✔ **Rotating log file support**
* ✔ **Runs in background as a systemd service**
* ✔ **Docker-ready**

---

# 📁 Project Structure


system-health-monitor/
├── monitor.py                # Main monitoring script
├── config.py                 # Configuration & thresholds
├── notifier.py               # Email + Webhook alert functions
├── logger_setup.py           # Logging configuration
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not committed)
├── README.md                 # Documentation
├── Dockerfile                # Build/run with Docker
├── scripts/
│   └── install.sh            # Automated installation script
└── systemd/
    └── system-health-monitor.service   # Systemd unit file


---

# 🛠 Requirements

* Python **3.9+**
* Linux/macOS/Windows
* psutil library
* For email: SMTP server (Gmail, Office365, etc.)
* Optional: Docker, systemd

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ⚙️ Configuration (`.env` file)

Create a `.env` file in project root:

MONITOR_INTERVAL=30

CPU_THRESHOLD_PERCENT=85
MEM_THRESHOLD_PERCENT=85
DISK_THRESHOLD_PERCENT=90

DISK_PARTITION=/

TOP_N_PROCESSES=5

SMTP_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=your_email@gmail.com
SMTP_TO=admin1@example.com,admin2@example.com

WEBHOOK_ENABLED=false
WEBHOOK_URL=https://hooks.slack.com/services/XXXXX/YYYYY/ZZZZZ

LOG_FILE=system-health-monitor.log
LOG_LEVEL=INFO

# ▶️ Running the Script Manually
bash
python monitor.py


Exit using `CTRL + C`.

---

# 🤖 Run as systemd Service (Linux)

1. Copy service file:

bash
sudo cp systemd/system-health-monitor.service /etc/systemd/system/
`

2. Reload systemd:
bash
sudo systemctl daemon-reload

3. Enable auto-start:

bash
sudo systemctl enable system-health-monitor


4. Start service:

```bash
sudo systemctl start system-health-monitor
```

5. View logs:

```bash
sudo journalctl -u system-health-monitor -f
```

---

# 🐳 Docker Deployment

Build image:

```bash
docker build -t system-health-monitor .
```

Run container:

```bash
docker run -d \
  --name system-health-monitor \
  --restart unless-stopped \
  --env-file .env \
  system-health-monitor
```

---

# 📝 Logging

Logs are stored using Python RotatingFileHandler.

Default log file:

```
system-health-monitor.log
```

It automatically rotates when size exceeds 5MB.

---

# 🔔 Alerts

## Email Alerts

Triggered when:

* CPU ≥ threshold
* Memory ≥ threshold
* Disk ≥ threshold

Email contains:

* Timestamp
* CPU/MEM/DISK summary
* Top N processes

## Webhook Alerts

Supports:

* Slack
* Microsoft Teams
* Custom HTTP endpoints

---

# 🔍 Example Alert Output

```
[ALERT] System health issue on server-01
Time: 2025-01-12T10:14:22Z

CPU: 92%
Memory: used=7.4GB total=8GB percent=89%
Disk (/): used=95GB total=100GB percent=95%

Top processes:
  1812 python3 cpu%=67 mem%=12
  3221 chrome cpu%=10 mem%=6
```

---

# 🧪 Testing Alerts

### Test CPU alert:

Set `.env`:

```
CPU_THRESHOLD_PERCENT=1
```

Restart script:

```bash
python monitor.py
```

Alerts should fire immediately.

---

# 🔧 scripts/install.sh (Purpose)

Automates:

* Installing dependencies
* Setting permissions
* Copying systemd service file
* Enabling service

Run using:

```bash
bash scripts/install.sh
```

---

# 🐞 Troubleshooting

### ✔ No alerts received?

* Check spam folder
* Verify SMTP credentials
* Check internet connection
* Print logs:

  ```bash
  tail -f system-health-monitor.log
  ```

### ✔ psutil not installed?

Run:

```bash
pip install psutil
```

### ✔ Systemd not starting?

Check status:

```bash
sudo systemctl status system-health-monitor
```

---

# 📌 Future Improvements

* HTML email templates
* Prometheus metrics exporter
* Simple web dashboard (Flask UI)
* Alert cooldown to avoid spam
* Multi-disk monitoring

---

# 📄 License

MIT License
Free to use and modify.

---

If you want, I can also generate:
✅ A professional GitHub description + tags
✅ Badges for README (build, license, version)
✅ A beautiful README with icons & screenshots

Just tell me **“Make README Pro Version”**.
