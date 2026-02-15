"""
Application Health Checker Script

Checks the uptime and health of web applications by making HTTP requests
and evaluating status codes. Reports whether each application is 'up' or 'down'.
Supports checking multiple URLs and outputs a summarized report.
"""
import requests
import logging
import datetime
import os
import sys

# --- Configuration ---
LOG_FILE = os.path.join(os.path.dirname(__file__), "app_health.log")

DEFAULT_URLS = [
    "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login",
    "https://www.google.com",
    "https://httpstat.us/500",  # always returns 500 (for testing 'down' detection)
    "https://thisdomaindoesnotexist12345.com",  # unreachable (for testing error handling)
]

TIMEOUT_SECONDS = 10

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE),
    ],
)
logger = logging.getLogger("AppHealthChecker")


def check_url(url: str) -> dict:
    """
    Check a single URL and return its health status.

    Returns a dict with: url, status_code, response_time_ms, status ('up'/'down'), error
    """
    result = {
        "url": url,
        "status_code": None,
        "response_time_ms": None,
        "status": "down",
        "error": None,
    }

    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS, allow_redirects=True)
        result["status_code"] = response.status_code
        result["response_time_ms"] = round(response.elapsed.total_seconds() * 1000, 2)

        if 200 <= response.status_code < 400:
            result["status"] = "up"
        else:
            result["status"] = "down"

    except requests.ConnectionError as e:
        result["error"] = f"Connection error: {e}"
    except requests.Timeout:
        result["error"] = f"Timeout after {TIMEOUT_SECONDS}s"
    except requests.RequestException as e:
        result["error"] = str(e)

    return result


def check_all(urls: list[str]) -> list[dict]:
    """Check all URLs and return a list of results."""
    results = []
    for url in urls:
        logger.info(f"Checking: {url}")
        result = check_url(url)

        if result["status"] == "up":
            logger.info(
                f"  Status: UP | HTTP {result['status_code']} | "
                f"Response: {result['response_time_ms']}ms"
            )
        else:
            error_info = result["error"] or f"HTTP {result['status_code']}"
            logger.warning(f"  Status: DOWN | {error_info}")

        results.append(result)
    return results


def print_report(results: list[dict]):
    """Print a summary report of all health checks."""
    logger.info("")
    logger.info("=" * 70)
    logger.info(f"Application Health Report - {datetime.datetime.now()}")
    logger.info("=" * 70)
    logger.info(f"{'URL':<50} {'Status':<8} {'Code':<6} {'Time (ms)':<10}")
    logger.info("-" * 70)

    up_count = 0
    down_count = 0

    for r in results:
        status = r["status"].upper()
        code = str(r["status_code"] or "N/A")
        time = str(r["response_time_ms"] or "N/A")
        logger.info(f"{r['url']:<50} {status:<8} {code:<6} {time:<10}")

        if r["status"] == "up":
            up_count += 1
        else:
            down_count += 1

    logger.info("-" * 70)
    logger.info(f"Total: {len(results)} | Up: {up_count} | Down: {down_count}")
    logger.info("=" * 70)


def main(urls: list[str] | None = None):
    """Main entry point."""
    if urls is None:
        urls = DEFAULT_URLS

    results = check_all(urls)
    print_report(results)
    return results


if __name__ == "__main__":
    # Accept URLs as command-line arguments, or use defaults
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main()
