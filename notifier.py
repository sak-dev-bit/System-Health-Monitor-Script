# notifier.py
import smtplib
from email.message import EmailMessage
import requests
import config
from logger_setup import get_logger

logger = get_logger("notifier")

def format_alert_subject():
    return f"[ALERT] System health issue on {config.HOSTNAME}"

def format_alert_body(metrics_snapshot: dict) -> str:
    # metrics_snapshot is a dict with keys cpu, memory, disk, top_processes, timestamp
    lines = []
    lines.append(f"Host: {config.HOSTNAME}")
    lines.append(f"Time: {metrics_snapshot.get('timestamp')}")
    lines.append(f"CPU: {metrics_snapshot.get('cpu')}%")
    mem = metrics_snapshot.get("memory", {})
    lines.append(f"Memory: used={mem.get('used_gb')}GB total={mem.get('total_gb')}GB percent={mem.get('percent')}%")
    disk = metrics_snapshot.get("disk", {})
    lines.append(f"Disk ({config.DISK_PARTITION}): used={disk.get('used_gb')}GB total={disk.get('total_gb')}GB percent={disk.get('percent')}%")
    lines.append("Top processes:")
    for p in metrics_snapshot.get("top_processes", []):
        lines.append(f"  {p['pid']} {p['name']} cpu%={p['cpu_percent']} mem%={p['memory_percent']}")

    return "\n".join(lines)

def send_email_alert(metrics_snapshot: dict):
    if not config.SMTP_ENABLED:
        logger.debug("SMTP not enabled; skipping email alert.")
        return False

    subject = format_alert_subject()
    body = format_alert_body(metrics_snapshot)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config.SMTP_FROM
    msg["To"] = ", ".join(config.SMTP_TO)
    msg.set_content(body)

    try:
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=10) as smtp:
            smtp.starttls()
            if config.SMTP_USER and config.SMTP_PASSWORD:
                smtp.login(config.SMTP_USER, config.SMTP_PASSWORD)
            smtp.send_message(msg)
        logger.info(f"Email alert sent to {config.SMTP_TO}")
        return True
    except Exception as e:
        logger.exception("Failed to send email alert: %s", e)
        return False

def send_webhook_alert(metrics_snapshot: dict):
    if not config.WEBHOOK_ENABLED or not config.WEBHOOK_URL:
        logger.debug("Webhook not enabled; skipping webhook alert.")
        return False

    payload = {
        "text": format_alert_subject(),
        "attachments": [
            {"text": format_alert_body(metrics_snapshot)}
        ]
    }
    try:
        r = requests.post(config.WEBHOOK_URL, json=payload, timeout=10)
        r.raise_for_status()
        logger.info(f"Webhook alert posted, status={r.status_code}")
        return True
    except Exception as e:
        logger.exception("Failed to send webhook alert: %s", e)
        return False

def notify_all(metrics_snapshot: dict):
    # call both methods (if enabled)
    email_ok = send_email_alert(metrics_snapshot)
    webhook_ok = send_webhook_alert(metrics_snapshot)
    return {"email": email_ok, "webhook": webhook_ok}
