"""
System Health Monitoring Script

Monitors CPU usage, memory usage, disk space, and running processes.
Alerts when metrics exceed predefined thresholds.
Logs results to console and a log file.
"""
import psutil
import logging
import datetime
import os

# --- Configuration ---
CPU_THRESHOLD = 80       # percent
MEMORY_THRESHOLD = 80    # percent
DISK_THRESHOLD = 80      # percent
TOP_PROCESSES = 5        # number of top processes to display
LOG_FILE = os.path.join(os.path.dirname(__file__), "system_health.log")

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE),
    ],
)
logger = logging.getLogger("SystemHealthMonitor")


def check_cpu():
    """Check CPU usage and alert if above threshold."""
    usage = psutil.cpu_percent(interval=1)
    logger.info(f"CPU Usage: {usage}%")
    if usage > CPU_THRESHOLD:
        logger.warning(f"ALERT: CPU usage {usage}% exceeds threshold of {CPU_THRESHOLD}%")
    return usage


def check_memory():
    """Check memory usage and alert if above threshold."""
    mem = psutil.virtual_memory()
    usage = mem.percent
    logger.info(
        f"Memory Usage: {usage}% "
        f"(Total: {mem.total / (1024**3):.2f} GB, "
        f"Available: {mem.available / (1024**3):.2f} GB)"
    )
    if usage > MEMORY_THRESHOLD:
        logger.warning(f"ALERT: Memory usage {usage}% exceeds threshold of {MEMORY_THRESHOLD}%")
    return usage


def check_disk():
    """Check disk space usage for all partitions and alert if above threshold."""
    alerts = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            pct = usage.percent
            logger.info(
                f"Disk [{partition.mountpoint}]: {pct}% used "
                f"(Total: {usage.total / (1024**3):.2f} GB, "
                f"Free: {usage.free / (1024**3):.2f} GB)"
            )
            if pct > DISK_THRESHOLD:
                logger.warning(
                    f"ALERT: Disk {partition.mountpoint} usage {pct}% "
                    f"exceeds threshold of {DISK_THRESHOLD}%"
                )
                alerts.append(partition.mountpoint)
        except PermissionError:
            logger.info(f"Disk [{partition.mountpoint}]: Permission denied, skipping")
    return alerts


def check_processes():
    """List top processes by CPU usage."""
    processes = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Sort by CPU usage descending
    processes.sort(key=lambda p: p.get("cpu_percent", 0) or 0, reverse=True)
    top = processes[:TOP_PROCESSES]

    logger.info(f"Top {TOP_PROCESSES} processes by CPU usage:")
    for p in top:
        logger.info(
            f"  PID {p['pid']:>6} | {p['name']:<25} | "
            f"CPU: {p.get('cpu_percent', 0):>5.1f}% | "
            f"MEM: {p.get('memory_percent', 0):>5.1f}%"
        )
    return top


def generate_report():
    """Run all checks and produce a summary report."""
    logger.info("=" * 60)
    logger.info(f"System Health Report - {datetime.datetime.now()}")
    logger.info("=" * 60)

    cpu = check_cpu()
    mem = check_memory()
    disk_alerts = check_disk()
    check_processes()

    logger.info("-" * 60)
    summary = "HEALTHY"
    if cpu > CPU_THRESHOLD or mem > MEMORY_THRESHOLD or disk_alerts:
        summary = "ALERTS DETECTED"
    logger.info(f"Overall Status: {summary}")
    logger.info("=" * 60)
    return summary


if __name__ == "__main__":
    generate_report()
