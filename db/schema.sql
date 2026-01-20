BEGIN;

CREATE TABLE IF NOT EXISTS data_version (
  id TEXT PRIMARY KEY,
  release_date DATE,
  is_active BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_data_version_active
  ON data_version (is_active)
  WHERE is_active;

CREATE TABLE IF NOT EXISTS occupation_master (
  data_version TEXT NOT NULL REFERENCES data_version(id) ON DELETE CASCADE,
  onetsoc_code VARCHAR(10) NOT NULL,
  soc_code VARCHAR(7),
  title TEXT NOT NULL,
  description TEXT,
  PRIMARY KEY (data_version, onetsoc_code)
);

CREATE INDEX IF NOT EXISTS idx_occupation_master_soc_code
  ON occupation_master (data_version, soc_code);

CREATE TABLE IF NOT EXISTS alternate_titles (
  data_version TEXT NOT NULL,
  onetsoc_code VARCHAR(10) NOT NULL,
  alternate_title VARCHAR(250) NOT NULL,
  short_title VARCHAR(150),
  PRIMARY KEY (data_version, onetsoc_code, alternate_title),
  FOREIGN KEY (data_version, onetsoc_code)
    REFERENCES occupation_master (data_version, onetsoc_code)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS task_statements (
  data_version TEXT NOT NULL REFERENCES data_version(id) ON DELETE CASCADE,
  task_id BIGINT NOT NULL,
  task_statement TEXT NOT NULL,
  PRIMARY KEY (data_version, task_id)
);

CREATE TABLE IF NOT EXISTS occupation_task_ratings (
  data_version TEXT NOT NULL,
  onetsoc_code VARCHAR(10) NOT NULL,
  task_id BIGINT NOT NULL,
  scale_id VARCHAR(3) NOT NULL,
  category INTEGER,
  data_value NUMERIC(6,2),
  n INTEGER,
  standard_error NUMERIC(7,4),
  lower_ci_bound NUMERIC(7,4),
  upper_ci_bound NUMERIC(7,4),
  recommend_suppress VARCHAR(1),
  date_updated DATE,
  domain_source VARCHAR(30),
  PRIMARY KEY (data_version, onetsoc_code, task_id, scale_id),
  FOREIGN KEY (data_version, onetsoc_code)
    REFERENCES occupation_master (data_version, onetsoc_code)
    ON DELETE CASCADE,
  FOREIGN KEY (data_version, task_id)
    REFERENCES task_statements (data_version, task_id)
    ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_occupation_task_ratings_task
  ON occupation_task_ratings (data_version, task_id);

CREATE INDEX IF NOT EXISTS idx_occupation_task_ratings_scale
  ON occupation_task_ratings (data_version, scale_id);

CREATE TABLE IF NOT EXISTS task_catalog (
  data_version TEXT NOT NULL,
  task_id BIGINT NOT NULL,
  score NUMERIC(8,4),
  source_scale_id VARCHAR(3),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (data_version, task_id),
  FOREIGN KEY (data_version, task_id)
    REFERENCES task_statements (data_version, task_id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS occupation_task_weight (
  data_version TEXT NOT NULL,
  soc_code VARCHAR(7) NOT NULL,
  task_id BIGINT NOT NULL,
  weight NUMERIC(10,8) NOT NULL,
  PRIMARY KEY (data_version, soc_code, task_id),
  FOREIGN KEY (data_version, task_id)
    REFERENCES task_statements (data_version, task_id)
    ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_occupation_task_weight_soc
  ON occupation_task_weight (data_version, soc_code);

CREATE TABLE IF NOT EXISTS model_run (
  id BIGSERIAL PRIMARY KEY,
  data_version TEXT NOT NULL REFERENCES data_version(id) ON DELETE CASCADE,
  model TEXT NOT NULL,
  prompt_version TEXT,
  model_version TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  cost_estimate NUMERIC(10,4),
  status TEXT,
  error_message TEXT,
  error_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS task_ai_score (
  id BIGSERIAL PRIMARY KEY,
  data_version TEXT NOT NULL,
  task_id BIGINT NOT NULL,
  model TEXT NOT NULL,
  score NUMERIC(6,2),
  run_id BIGINT REFERENCES model_run(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  raw_json_ref TEXT,
  prompt_hash TEXT,
  input_hash TEXT,
  FOREIGN KEY (data_version, task_id)
    REFERENCES task_statements (data_version, task_id)
    ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_task_ai_score_cache
  ON task_ai_score (data_version, task_id, model, prompt_hash, input_hash);

CREATE INDEX IF NOT EXISTS idx_task_ai_score_task
  ON task_ai_score (data_version, task_id);

CREATE TABLE IF NOT EXISTS task_ai_ensemble (
  data_version TEXT NOT NULL,
  task_id BIGINT NOT NULL,
  mean NUMERIC(6,2),
  std NUMERIC(6,2),
  min NUMERIC(6,2),
  max NUMERIC(6,2),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (data_version, task_id),
  FOREIGN KEY (data_version, task_id)
    REFERENCES task_statements (data_version, task_id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS occupation_ai_score (
  data_version TEXT NOT NULL,
  soc_code VARCHAR(7) NOT NULL,
  mean NUMERIC(6,2),
  std NUMERIC(6,2),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (data_version, soc_code),
  FOREIGN KEY (data_version) REFERENCES data_version(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_occupation_ai_score_mean
  ON occupation_ai_score (data_version, mean DESC);

CREATE TABLE IF NOT EXISTS bls_oews_metrics (
  soc_code VARCHAR(7) NOT NULL,
  ref_year_month VARCHAR(7) NOT NULL,
  employment INTEGER,
  median_wage INTEGER,
  mean_wage INTEGER,
  PRIMARY KEY (soc_code, ref_year_month)
);

CREATE TABLE IF NOT EXISTS bls_proj_metrics (
  soc_code VARCHAR(7) NOT NULL,
  projection_period VARCHAR(20) NOT NULL,
  growth_pct NUMERIC(6,2),
  annual_openings INTEGER,
  PRIMARY KEY (soc_code, projection_period)
);

COMMIT;
