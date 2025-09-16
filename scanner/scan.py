from __future__ import annotations
import argparse, time, os, csv
from .zap_client import ZAPClient

PROFILES = {
    "fast": {"spider_max_children": 10, "active_rules": "Default"},
    "thorough": {"spider_max_children": 100, "active_rules": "All"},
}


def run_scan(target: str, minutes: int, profile: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    client = ZAPClient()
    client.wait_until_ready()
    zap = client.zap

    # Open target in ZAP (so it’s in context)
    zap.urlopen(target)
    # NOTE: DVWA has to be set to "low" security or this won't catch much


    # Spider
    spider_id = zap.spider.scan(target, maxchildren=PROFILES[profile]["spider_max_children"])  # type: ignore
    while int(zap.spider.status(spider_id)) < 100:
        time.sleep(1)

    # Passive scan wait
    while int(zap.pscan.records_to_scan) > 0:
        time.sleep(1)

    # Active scan
    ascan_id = zap.ascan.scan(target, recurse=True)

    deadline = time.time() + minutes * 60
    while time.time() < deadline:
        status = int(zap.ascan.status(ascan_id))
        if status >= 100:
            break
        time.sleep(1)

    alerts = zap.core.alerts(baseurl=target, start=0, count=9999)
    out_csv = os.path.join(out_dir, "alerts.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sorted({k for a in alerts for k in a.keys()}))
        writer.writeheader()
        for a in alerts:
            writer.writerow(a)

    #took forever to get ZAP to talk to Python
    print(f"Saved alerts to {out_csv}; count={len(alerts)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=os.getenv("TARGET_URL", "http://localhost:8081"))
    ap.add_argument("--minutes", type=int, default=2)
    ap.add_argument("--profile", choices=PROFILES.keys(), default="fast")
    ap.add_argument("--out", default="./reports/samples")
    args = ap.parse_args()
    run_scan(args.target, args.minutes, args.profile, args.out)
