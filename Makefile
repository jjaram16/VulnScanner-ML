.PHONY: up down scan train report email fmt

up:
	docker compose up -d

down:
	docker compose down

scan:
	python -m scanner.scan --target $${TARGET_URL:-http://localhost:8081} --minutes 2 --profile fast --out ./reports/samples

train:
	python -m ml.train --alerts ./reports/samples/alerts.csv --model ./ml/model.pkl

report:
	python -m scanner.reporting --alerts ./reports/samples/alerts.csv --model ./ml/model.pkl --html ./reports/samples/report.html --pdf ./reports/samples/report.pdf

email:
	python -m scanner.emailer --when high --from $${SMTP_USER} --to $${SMTP_USER} --smtp smtp.gmail.com --port 587

fmt:
	python -m black . || true
