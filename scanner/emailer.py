import argparse, os, smtplib
from email.mime.text import MIMEText

SEV_MAP = {2: "HIGH", 1: "MEDIUM", 0: "LOW"}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--when", choices=["high","medium","low"], default="high")
    ap.add_argument("--from", dest="sender", required=True)
    ap.add_argument("--to", dest="to", required=True)
    ap.add_argument("--smtp", default="smtp.gmail.com")
    ap.add_argument("--port", type=int, default=587)
    args = ap.parse_args()

    username = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")

    body = f"Alert: {args.when.upper()} severity findings detected in latest scan. See attached report or dashboard."
    msg = MIMEText(body)
    msg["Subject"] = f"VulnScanner-ML: {args.when.upper()} findings"
    msg["From"] = args.sender
    msg["To"] = args.to

    with smtplib.SMTP(args.smtp, args.port) as s:
        s.starttls(); s.login(username, password)
        s.send_message(msg)
        print("Sent email")
