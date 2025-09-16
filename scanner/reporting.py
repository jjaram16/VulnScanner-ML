import argparse
import pandas as pd
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from jinja2 import Template
from scanner.model import RiskClassifier

HTML_TEMPLATE = """
<!doctype html>
<html><head><meta charset="utf-8"><title>Vuln Report</title>
<style>body{font-family: system-ui; margin: 24px;} table{border-collapse: collapse; width: 100%;} th,td{border:1px solid #ddd;padding:8px;} th{background:#f5f5f5;text-align:left} .sev2{color:#b00020}.sev1{color:#c98000}.sev0{color:#2b6cb0}
small{color:#666}
</style></head>
<body>
<h1>Vulnerability Report</h1>
<p><small>Generated on {{ generated }}</small></p>
<table>
  <thead><tr><th>Risk</th><th>Alert</th><th>URL</th><th>Param</th><th>Pred. Severity</th></tr></thead>
  <tbody>
  {% for r in rows %}
    <tr>
      <td>{{ r.risk }}</td><td>{{ r.alert }}</td><td>{{ r.url }}</td><td>{{ r.param }}</td>
      <td class="sev{{ r.pred }}">{{ r.pred }}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>
</body></html>
"""


def write_pdf(rows, path_pdf):
    c = canvas.Canvas(path_pdf, pagesize=LETTER)
    w, h = LETTER
    y = h - 72
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, y, "Vulnerability Report")
    y -= 24
    c.setFont("Helvetica", 9)
    for r in rows[:40]:  # avoid overflow
        line = f"{r['risk']:<6} | {r['alert'][:40]:<40} | {r['url'][:50]}"
        if y < 72:
            c.showPage(); y = h - 72
        c.drawString(72, y, line)
        y -= 12
    c.save()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--alerts", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--html", required=True)
    ap.add_argument("--pdf", required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.alerts)
    clf = RiskClassifier.load(args.model)
    preds = clf.predict(df)

    rows = df.assign(pred=preds).to_dict(orient="records")

    from datetime import datetime
    html = Template(HTML_TEMPLATE).render(rows=rows, generated=datetime.utcnow().isoformat())
    with open(args.html, "w", encoding="utf-8") as f:
        f.write(html)

    write_pdf(rows, args.pdf)
    print(f"Wrote {args.html} and {args.pdf}")
