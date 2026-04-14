# encoding: utf-8
import os
import time
import threading
import concurrent.futures
from datetime import datetime

import requests
import openpyxl
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt


# ── Config ───────────────────────────────────────────────────────────────────
BASE_URL = "https://api.xinvoice.vn/gdt-api/tax-payer"
HEADERS = {
    "client-id": "61251923-92ee-4975-8b67-c90e4e5a7639",
    "api-key": "de87383b-8e66-4b97-83e1-06252a44efb6",
}

INPUT_FILE = os.path.join(os.path.dirname(__file__), "data.xlsx")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "data_output.xlsx")

MAX_WORKERS = 60
RATE_LIMIT = 95          # requests per window (safety margin from 100)
RATE_WINDOW = 30          # seconds

# Column indices (1-based)
COL_PROJECT_NAME = 1      # A
COL_FULL_NAME = 2         # B
COL_TAX_CODE = 3          # C
COL_ORG_TYPE = 4          # D
COL_TAX_ID = 5            # E
COL_NAME = 6              # F
COL_ADDRESS = 7           # G
COL_TAX_DEPT = 8          # H
COL_STATUS = 9            # I
COL_UPDATED_AT = 10       # J
COL_LOG = 11              # K


# ── Rate Limiter (Token Bucket) ─────────────────────────────────────────────
class RateLimiter:
    def __init__(self, max_tokens: int, window_seconds: float):
        self._max_tokens = max_tokens
        self._window = window_seconds
        self._tokens: list[float] = []
        self._lock = threading.Lock()

    def acquire(self):
        while True:
            with self._lock:
                now = time.monotonic()
                # Remove expired tokens
                self._tokens = [t for t in self._tokens if now - t < self._window]
                if len(self._tokens) < self._max_tokens:
                    self._tokens.append(now)
                    return
            # Wait a bit before retrying
            time.sleep(0.35)


# ── API Call ─────────────────────────────────────────────────────────────────
class RateLimitError(Exception):
    """Raised when API returns 429 Too Many Requests."""
    pass


@retry(
    retry=retry_if_exception_type(RateLimitError),
    wait=wait_exponential(multiplier=5, min=5, max=60),
    stop=stop_after_attempt(6),
    reraise=True,
)
def _call_api(tax_code: str) -> requests.Response:
    """Make the HTTP request, raising RateLimitError on 429 for tenacity retry."""
    resp = requests.get(f"{BASE_URL}/{tax_code}", headers=HEADERS, timeout=30)
    if resp.status_code == 429:
        raise RateLimitError(f"429 Too Many Requests for {tax_code}")
    return resp


def lookup_tax(tax_code: str) -> dict:
    """Call XInvoice API and return parsed result dict."""
    try:
        resp = _call_api(tax_code)
        data = resp.json()

        if "error" in data:
            return {"success": False, "error": data["error"]}

        resp.raise_for_status()

        return {
            "success": True,
            "orgType": data.get("orgType"),
            "taxID": data.get("taxID"),
            "name": data.get("name"),
            "address": data.get("address"),
            "taxDepartment": data.get("taxDepartment"),
            "status": data.get("status"),
            "updatedAt": data.get("updatedAt"),
        }
    except RateLimitError:
        return {"success": False, "error": "Rate limited (429) - max retries exceeded"}
    except requests.RequestException as e:
        return {"success": False, "error": f"Request error - {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error - {e}"}


# ── Process a single row ────────────────────────────────────────────────────
def process_row(row_data: list, rate_limiter: RateLimiter) -> list:
    """Query API for one row and return the updated row."""
    tax_code = str(row_data[COL_TAX_CODE - 1] or "").strip()
    if not tax_code:
        row_data[COL_LOG - 1] = "Empty tax code"
        return row_data

    rate_limiter.acquire()
    result = lookup_tax(tax_code)

    if result["success"]:
        row_data[COL_ORG_TYPE - 1] = result["orgType"]
        row_data[COL_TAX_ID - 1] = result["taxID"]
        row_data[COL_NAME - 1] = result["name"]
        row_data[COL_ADDRESS - 1] = result["address"]
        row_data[COL_TAX_DEPT - 1] = result["taxDepartment"]
        row_data[COL_STATUS - 1] = result["status"]
        row_data[COL_UPDATED_AT - 1] = result["updatedAt"]
        row_data[COL_LOG - 1] = "Success"
    else:
        row_data[COL_LOG - 1] = result["error"]

    return row_data


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print(f"[{datetime.now():%H:%M:%S}] Loading {INPUT_FILE} ...")
    wb = openpyxl.load_workbook(INPUT_FILE)
    ws = wb.active

    # Read headers
    headers = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]

    # Read all data rows, preserving original order index
    all_rows: list[tuple[int, list, bool]] = []  # (index, row_data, is_success)
    for row_idx in range(2, ws.max_row + 1):
        row_data = [ws.cell(row=row_idx, column=c).value for c in range(1, ws.max_column + 1)]
        log_val = str(row_data[COL_LOG - 1] or "").strip().lower()
        is_success = log_val == "success"
        all_rows.append((row_idx, row_data, is_success))

    success_count = sum(1 for _, _, s in all_rows if s)
    pending_count = len(all_rows) - success_count
    print(f"[{datetime.now():%H:%M:%S}] Total rows: {len(all_rows)} | "
          f"Already success: {success_count} | To query: {pending_count}")
    return

    # Separate
    pending_items = [(idx, row_data) for idx, row_data, is_success in all_rows if not is_success]

    # Rate limiter
    rate_limiter = RateLimiter(RATE_LIMIT, RATE_WINDOW)

    # Results dict: original_index -> row_data
    results: dict[int, list] = {}

    # Copy success rows directly
    for idx, row_data, is_success in all_rows:
        if is_success:
            results[idx] = row_data

    # Process pending rows with thread pool
    completed = 0
    total_pending = len(pending_items)
    counter_lock = threading.Lock()

    def _task(item):
        nonlocal completed
        idx, row_data = item
        updated = process_row(row_data, rate_limiter)
        with counter_lock:
            completed += 1
            current = completed
        if current % 100 == 0 or current == total_pending:
            print(f"[{datetime.now():%H:%M:%S}] Progress: {current}/{total_pending} "
                  f"({current * 100 // total_pending}%)")
        return idx, updated

    print(f"[{datetime.now():%H:%M:%S}] Starting {MAX_WORKERS} workers ...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(_task, item): item for item in pending_items}
        for future in concurrent.futures.as_completed(futures):
            try:
                idx, updated_row = future.result()
                results[idx] = updated_row
            except Exception as e:
                item = futures[future]
                idx, row_data = item
                row_data[COL_LOG - 1] = f"Thread error - {e}"
                results[idx] = row_data

    # Write output
    print(f"[{datetime.now():%H:%M:%S}] Writing {OUTPUT_FILE} ...")
    wb_out = openpyxl.Workbook()
    ws_out = wb_out.active
    ws_out.title = ws.title

    # Write headers
    for c, header in enumerate(headers, 1):
        ws_out.cell(row=1, column=c, value=header)

    # Write data rows in original order
    out_row = 2
    for idx in sorted(results.keys()):
        row_data = results[idx]
        for c, val in enumerate(row_data, 1):
            ws_out.cell(row=out_row, column=c, value=val)
        out_row += 1

    wb_out.save(OUTPUT_FILE)
    wb.close()

    # Summary
    final_success = sum(1 for rd in results.values() if str(rd[COL_LOG - 1] or "").strip().lower() == "success")
    print(f"[{datetime.now():%H:%M:%S}] Done! Output: {OUTPUT_FILE}")
    print(f"  Total: {len(results)} | Success: {final_success} | "
          f"Failed: {len(results) - final_success}")


if __name__ == "__main__":
    main()
