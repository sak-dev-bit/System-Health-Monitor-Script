# monitor.py
import time
import psutil
import datetime
import config
from logger_setup import get_logger
from notifier import notify_all
import signal
import sys

logger = get_logger("monitor")

running = True

def handle_sigterm(signum, frame):
    global running
    logger.info("Received termination signal. Exiting gracefully...")
    running = False

signal.signal(signal.SIGINT, handle_sigterm)
signal.signal(signal.SIGTERM, handle_sigterm)

def bytes_to_gb(b):
    return round(b / (1024**3), 2)

def get_cpu_percent():
    # psutil.cpu_percent with interval=1 blocks for one second; use percpu=False for overall
    return psutil.cpu_percent(interval=None)  # non-blocking (returns last interval)

def get_memory_info():
    vm = psutil.virtual_memory()
    return {
        "total_gb": bytes_to_gb(vm.total),
        "available_gb": bytes_to_gb(vm.available),
        "used_gb": bytes_to_gb(vm.used),
        "percent": vm.percent
    }

def get_disk_info(partition=config.DISK_PARTITION):
    du = psutil.disk_usage(partition)
    return {
        "total_gb": bytes_to_gb(du.total),
        "used_gb": bytes_to_gb(du.used),
        "free_gb": bytes_to_gb(du.free),
        "percent": du.percent
    }

def get_top_processes(n=config.TOP_N_PROCESSES):
    procs = []
    for p in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            info = p.info
            # cpu_percent may be 0.0 if not measured; call once to cache for next call
            procs.append({
                "pid": info.get("pid"),
                "name": info.get("name"),
                "cpu_percent": round(info.get("cpu_percent", 0.0), 2),
                "memory_percent": round(info.get("memory_percent", 0.0), 2),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    # sort by cpu then memory
    procs_sorted = sorted(procs, key=lambda x: (x["cpu_percent"], x["memory_percent"]), reverse=True)
    return procs_sorted[:n]

def should_alert(metrics):
    # Returns True if any metric exceeds threshold
    if metrics["cpu"] >= config.CPU_THRESHOLD_PERCENT:
        logger.debug("CPU threshold breached: %s%% >= %s%%", metrics["cpu"], config.CPU_THRESHOLD_PERCENT)
        return True, "cpu"
    if metrics["memory"]["percent"] >= config.MEM_THRESHOLD_PERCENT:
        logger.debug("Memory threshold breached: %s%% >= %s%%", metrics["memory"]["percent"], config.MEM_THRESHOLD_PERCENT)
        return True, "memory"
    if metrics["disk"]["percent"] >= config.DISK_THRESHOLD_PERCENT:
        logger.debug("Disk threshold breached: %s%% >= %s%%", metrics["disk"]["percent"], config.DISK_THRESHOLD_PERCENT)
        return True, "disk"
    return False, None

def build_snapshot():
    snapshot = {}
    snapshot["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
    snapshot["cpu"] = get_cpu_percent()
    snapshot["memory"] = get_memory_info()
    snapshot["disk"] = get_disk_info()
    snapshot["top_processes"] = get_top_processes()
    return snapshot

def main_loop():
    logger.info("Starting system health monitor. Polling every %s seconds", config.INTERVAL)
    # Warm up cpu_percent sampling
    psutil.cpu_percent(interval=0.1)
    while running:
        metrics = build_snapshot()
        logger.info("Snapshot: CPU=%s%%, MEM=%s%%, DISK=%s%%",
                    metrics["cpu"], metrics["memory"]["percent"], metrics["disk"]["percent"])
        alert, reason = should_alert(metrics)
        if alert:
            logger.warning("Threshold breached (%s). Sending alerts.", reason)
            notify_all(metrics)
        # sleep loop but be responsive to signals
        slept = 0
        while slept < config.INTERVAL and running:
            time.sleep(1)
            slept += 1

if __name__ == "__main__":
    try:
        main_loop()
    except Exception as e:
        logger.exception("Unhandled exception in monitor: %s", e)
        sys.exit(1)
