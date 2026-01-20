# task-risk

AI automation risk service for occupations/tasks/skills using O*NET and BLS data.

## macOS setup (Homebrew)

Commands
- `brew install postgresql@18`
- `brew services start postgresql@18`
- `export PATH="/opt/homebrew/opt/postgresql@18/bin:$PATH"`  # or add to ~/.zshrc
- `createuser -P task_risk`
- `createdb -O task_risk task_risk`

Notes
- If `psql` is not found, use `/opt/homebrew/opt/postgresql@18/bin/psql`.

---

## Local quick start (no Docker)
1. Install Postgres 18 (latest) and ensure `psql` is available.
2. Create DB/user (example):
   - `createuser -P task_risk`
   - `createdb -O task_risk task_risk`
3. `cp .env.example .env` and set `DATABASE_URL` or `POSTGRES_*`, plus `ONET_DATA_VERSION`/`DEFAULT_DATA_VERSION`.
4. `python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt`
5. `./scripts/apply_schema.sh`
6. `./.venv/bin/python -m batch.import_onet --data-version 30.1`
7. `./.venv/bin/python -m batch.set_active_version --data-version 30.1`
8. `./.venv/bin/python -m batch.update_soc_codes --data-version 30.1`
9. `./.venv/bin/python -m batch.build_task_catalog --size 200 --data-version 30.1`
10. `./.venv/bin/python -m batch.build_task_weights --data-version 30.1`
11. `./.venv/bin/python -m worker.score_tasks --limit 20 --data-version 30.1`
12. `./.venv/bin/python -m worker.aggregate_occupations --data-version 30.1`
13. `./.venv/bin/uvicorn api.main:app --reload`

Notes:
- ETL uses truncate+reload for idempotent re-runs.
- O*NET SQL source defaults to `./Data/db_30_1_mysql`.
- LLM scoring is mocked by default (`USE_MOCK_LLM=1`).
- Real LLM providers are stubbed; set `USE_MOCK_LLM=0` only after implementing provider calls.
- API/ETL uses `DEFAULT_DATA_VERSION` unless a request or CLI overrides it.
- If you already applied the old schema, recreate the DB or add data_version columns via migration.
- LLM retry settings: `LLM_MAX_RETRIES`, `LLM_RETRY_BASE_DELAY`, `LLM_RETRY_MAX_DELAY`, `LLM_RETRY_JITTER`.

---

## Ubuntu server setup (no Docker)

Tested target: Ubuntu 24.04 LTS.

Files
- `deploy/systemd/task-risk-api.service`
- `deploy/nginx/task-risk.conf`
- `deploy/cron/task-risk.cron`

Steps
1. Install base packages:
   - `sudo apt-get update`
   - `sudo apt-get install -y ca-certificates curl gnupg python3-venv python3-pip nginx postgresql-common`
2. Enable PGDG repo and install latest Postgres (18, currently 18.1):
   - `sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh`
   - `sudo apt-get install -y postgresql-18`
3. Place the repo in `/opt/task-risk` (or update paths in deploy files).
4. Create venv and install deps:
   - `python3 -m venv /opt/task-risk/.venv`
   - `/opt/task-risk/.venv/bin/pip install -r /opt/task-risk/requirements.txt`
5. Create `/opt/task-risk/.env` and set DB credentials plus data versions.
6. Apply schema and run ETL (same as local quick start).
7. Install systemd unit:
   - `sudo cp deploy/systemd/task-risk-api.service /etc/systemd/system/`
   - `sudo systemctl daemon-reload`
   - `sudo systemctl enable --now task-risk-api`
8. Optional: nginx reverse proxy:
   - `sudo cp deploy/nginx/task-risk.conf /etc/nginx/sites-available/task-risk`
   - `sudo ln -s /etc/nginx/sites-available/task-risk /etc/nginx/sites-enabled/task-risk`
   - `sudo nginx -t && sudo systemctl reload nginx`
9. Optional: cron schedule:
   - `sudo mkdir -p /var/log/task-risk`
   - `sudo cp deploy/cron/task-risk.cron /etc/cron.d/task-risk`
10. Firewall (example):
   - `sudo ufw allow OpenSSH`
   - `sudo ufw allow 80`
   - `sudo ufw enable`

Notes:
- Update `User=ubuntu` and `WorkingDirectory=/opt/task-risk` in the systemd unit to match your server.
- Replace `server_name` in the nginx config with your domain or IP.
- If you do not use nginx, open port 8000 instead of 80.
- PGDG will install the latest 18.x minor (18.1 as of 2025-11-13).

---

## Day 1: Base/Schema (includes O*NET core table doc)

Files
- `.env.example`
- `requirements.txt`
- `db/schema.sql`
- `scripts/apply_schema.sh`
- `api/main.py`
- `api/db.py`
- `docs/onet_core_tables.md`

Commands
- `cp .env.example .env`
- `./scripts/apply_schema.sh`
- `uvicorn api.main:app --reload`

Verification queries
```sql
SELECT COUNT(*) FROM occupation_master WHERE data_version = '30.1';
SELECT COUNT(*) FROM task_statements WHERE data_version = '30.1';
```

---

## Day 2: O*NET Load (ETL)

Files
- `batch/import_onet.py`
- `batch/set_active_version.py`
- `batch/utils.py`

Commands
- `python -m batch.import_onet --sql-dir ./Data/db_30_1_mysql --data-version 30.1`
- `python -m batch.set_active_version --data-version 30.1`

Verification queries
```sql
SELECT onetsoc_code, title FROM occupation_master
WHERE data_version = '30.1'
ORDER BY onetsoc_code
LIMIT 10;

SELECT otr.task_id, ts.task_statement, otr.data_value
FROM occupation_task_ratings otr
JOIN task_statements ts
  ON ts.data_version = otr.data_version
 AND ts.task_id = otr.task_id
WHERE otr.data_version = '30.1'
  AND otr.onetsoc_code = '11-1011.00'
  AND otr.scale_id = 'IM'
ORDER BY otr.data_value DESC NULLS LAST
LIMIT 20;
```

---

## Day 3: BLS Stubs + SOC Mapping

Files
- `batch/update_soc_codes.py`
- `batch/import_bls_stub.py`

Commands
- `python -m batch.update_soc_codes --data-version 30.1`
- `python batch/import_bls_stub.py --oews path/to/oews.csv --projections path/to/proj.csv`

Verification queries
```sql
SELECT onetsoc_code, soc_code FROM occupation_master WHERE data_version = '30.1' ORDER BY onetsoc_code LIMIT 10;
SELECT COUNT(*) FROM bls_oews_metrics;
SELECT COUNT(*) FROM bls_proj_metrics;
```

---

## Day 4: Task Catalog/Weights

Files
- `batch/build_task_catalog.py`
- `batch/build_task_weights.py`

Commands
- `python -m batch.build_task_catalog --size 200 --scale-id IM --data-version 30.1`
- `python -m batch.build_task_weights --scale-id IM --data-version 30.1`

Verification queries
```sql
SELECT COUNT(*) FROM task_catalog WHERE data_version = '30.1';
SELECT soc_code, SUM(weight) AS weight_sum
FROM occupation_task_weight
WHERE data_version = '30.1'
GROUP BY soc_code
ORDER BY weight_sum DESC
LIMIT 5;
```

---

## Day 5: LLM Scoring + API MVP

Files
- `worker/score_tasks.py`
- `worker/aggregate_occupations.py`
- `api/main.py`

LLM 설정 (실서비스 모드)
- `.env`에서 `USE_MOCK_LLM=0` 설정
- `LLM_PROVIDERS_ENABLED=openai,anthropic` (필요 시 `local` 추가)
- 기본 모델
  - `LLM_OPENAI_MODEL=gpt-5-nano`
  - `LLM_ANTHROPIC_MODEL=claude-haiku-4-5`
- 키
  - `OPENAI_API_KEY=...`
  - `ANTHROPIC_API_KEY=...`
- OpenAI 프록시/게이트웨이 사용 시
  - `LLM_OPENAI_BASE_URL=...`
- 로컬/OpenAI 호환 서버 사용 시
  - `LLM_PROVIDERS_ENABLED=local`
  - `LLM_LOCAL_BASE_URL=http://localhost:11434/v1`
  - `LLM_LOCAL_MODEL=...`
  - `LLM_LOCAL_API_KEY=local` (필요 시)
- GPT-5 계열은 `temperature`를 지원하지 않으므로 기본값은 비워둠 (`LLM_TEMPERATURE=`)

Commands
- `python -m worker.score_tasks --models openai,claude --limit 20 --data-version 30.1`
- `python -m worker.score_tasks --models openai:gpt-5-nano,claude:claude-haiku-4-5 --limit 20 --data-version 30.1`
- `python -m worker.aggregate_occupations --data-version 30.1`
- `uvicorn api.main:app --reload`

Verification queries
```sql
SELECT COUNT(*) FROM task_ai_score WHERE data_version = '30.1';
SELECT COUNT(*) FROM task_ai_ensemble WHERE data_version = '30.1';
SELECT * FROM occupation_ai_score WHERE data_version = '30.1' ORDER BY mean DESC NULLS LAST LIMIT 10;
```

API checks
- `curl http://localhost:8000/health`
- `curl "http://localhost:8000/occupations?sort=ai&page=1&data_version=30.1"`
- `curl "http://localhost:8000/occupations/11-1011?data_version=30.1"`
- `curl "http://localhost:8000/rankings/ai_risk?limit=20&data_version=30.1"`

---

## Smoke checks

Commands
- `python -m scripts.smoke_check --data-version 30.1`
- `python -m scripts.smoke_check --data-version 30.1 --require-ai`

## Offline checks (no DB)

Commands
- `python -m scripts.offline_check --sql-dir ./Data/db_30_1_mysql`
- `python -m scripts.offline_check --sql-dir ./Data/db_30_1_mysql --sample 200`
- `python -m scripts.offline_check --sql-dir ./Data/db_30_1_mysql --count-only`
- `python -m scripts.offline_check --sql-dir ./Data/db_30_1_mysql --compare-to ./Data/db_30_2_mysql`
- `python -m scripts.offline_check --sql-dir ./Data/db_30_1_mysql --compare-to ./Data/db_30_2_mysql --report-json ./tmp/onet_compare.json`

## Maintenance helpers

Commands
- `python -m batch.set_active_version --data-version 30.2`
- `python -m batch.archive_versions --keep-latest 4 --dry-run`
- `python -m batch.archive_versions --keep-latest 4`


---

## Ubuntu 24.04 서버: 한줄씩 실행 순서 (no Docker)

전제: 코드 위치는 `/opt/task-risk`, 사용자 `ubuntu` 기준.

1) 패키지 업데이트
`sudo apt-get update`

2) 기본 패키지 설치
`sudo apt-get install -y ca-certificates curl gnupg python3-venv python3-pip nginx postgresql-common`

3) PGDG 저장소 등록 및 PostgreSQL 18 설치
`sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh`
`sudo apt-get install -y postgresql-18`

4) 소스 배치
`sudo mkdir -p /opt/task-risk`
`sudo chown ubuntu:ubuntu /opt/task-risk`
`# (원하는 방식으로 코드 업로드/클론 후 /opt/task-risk 에 위치)`

5) 가상환경 생성 및 의존성 설치
`python3 -m venv /opt/task-risk/.venv`
`/opt/task-risk/.venv/bin/pip install -r /opt/task-risk/requirements.txt`

6) DB/유저 생성 (예시)
`createuser -P task_risk`
`createdb -O task_risk task_risk`

7) 환경 변수 파일 작성
`cp /opt/task-risk/.env.example /opt/task-risk/.env`
`# .env에서 DATABASE_URL 또는 POSTGRES_*, ONET_DATA_VERSION, DEFAULT_DATA_VERSION 설정`

8) 스키마 적용
`cd /opt/task-risk && ./scripts/apply_schema.sh`

9) O*NET 적재
`cd /opt/task-risk && ./.venv/bin/python -m batch.import_onet --sql-dir ./Data/db_30_1_mysql --data-version 30.1`

10) 활성 버전 지정
`cd /opt/task-risk && ./.venv/bin/python -m batch.set_active_version --data-version 30.1`

11) SOC 매핑 갱신
`cd /opt/task-risk && ./.venv/bin/python -m batch.update_soc_codes --data-version 30.1`

12) Task catalog 생성
`cd /opt/task-risk && ./.venv/bin/python -m batch.build_task_catalog --size 200 --data-version 30.1`

13) Task weight 생성
`cd /opt/task-risk && ./.venv/bin/python -m batch.build_task_weights --data-version 30.1`

14) LLM 점수화(샘플 20)
`cd /opt/task-risk && ./.venv/bin/python -m worker.score_tasks --limit 20 --data-version 30.1`

15) 직업 점수 집계
`cd /opt/task-risk && ./.venv/bin/python -m worker.aggregate_occupations --data-version 30.1`

16) API 실행(테스트)
`cd /opt/task-risk && ./.venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000`

17) systemd 등록
`sudo cp /opt/task-risk/deploy/systemd/task-risk-api.service /etc/systemd/system/`
`sudo systemctl daemon-reload`
`sudo systemctl enable --now task-risk-api`

18) nginx 연결(선택)
`sudo cp /opt/task-risk/deploy/nginx/task-risk.conf /etc/nginx/sites-available/task-risk`
`sudo ln -s /etc/nginx/sites-available/task-risk /etc/nginx/sites-enabled/task-risk`
`sudo nginx -t && sudo systemctl reload nginx`

19) cron 등록(선택)
`sudo mkdir -p /var/log/task-risk`
`sudo cp /opt/task-risk/deploy/cron/task-risk.cron /etc/cron.d/task-risk`

20) 방화벽(선택)
`sudo ufw allow OpenSSH`
`sudo ufw allow 80`
`sudo ufw enable`
