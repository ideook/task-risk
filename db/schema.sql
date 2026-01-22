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
  category INTEGER NOT NULL DEFAULT 0,
  data_value NUMERIC(6,2),
  n INTEGER,
  standard_error NUMERIC(7,4),
  lower_ci_bound NUMERIC(7,4),
  upper_ci_bound NUMERIC(7,4),
  recommend_suppress VARCHAR(1),
  date_updated DATE,
  domain_source VARCHAR(30),
  PRIMARY KEY (data_version, onetsoc_code, task_id, scale_id, category),
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
  week VARCHAR(8) NOT NULL,
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
  week VARCHAR(8) NOT NULL,
  task_id BIGINT NOT NULL,
  model TEXT NOT NULL,
  score NUMERIC(6,2),
  ai_substitution_risk NUMERIC(6,2),
  ai_augmentation_potential NUMERIC(6,2),
  human_context_dependency NUMERIC(6,2),
  physical_world_dependency NUMERIC(6,2),
  confidence NUMERIC(4,2),
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
  ON task_ai_score (data_version, week, task_id, model, prompt_hash, input_hash);

CREATE INDEX IF NOT EXISTS idx_task_ai_score_task
  ON task_ai_score (data_version, week, task_id);

CREATE TABLE IF NOT EXISTS task_ai_ensemble (
  data_version TEXT NOT NULL,
  week VARCHAR(8) NOT NULL,
  task_id BIGINT NOT NULL,
  mean NUMERIC(6,2),
  std NUMERIC(6,2),
  min NUMERIC(6,2),
  max NUMERIC(6,2),
  ai_augmentation_potential_mean NUMERIC(6,2),
  ai_augmentation_potential_std NUMERIC(6,2),
  ai_augmentation_potential_min NUMERIC(6,2),
  ai_augmentation_potential_max NUMERIC(6,2),
  human_context_dependency_mean NUMERIC(6,2),
  human_context_dependency_std NUMERIC(6,2),
  human_context_dependency_min NUMERIC(6,2),
  human_context_dependency_max NUMERIC(6,2),
  physical_world_dependency_mean NUMERIC(6,2),
  physical_world_dependency_std NUMERIC(6,2),
  physical_world_dependency_min NUMERIC(6,2),
  physical_world_dependency_max NUMERIC(6,2),
  confidence_mean NUMERIC(6,2),
  confidence_std NUMERIC(6,2),
  confidence_min NUMERIC(6,2),
  confidence_max NUMERIC(6,2),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (data_version, week, task_id),
  FOREIGN KEY (data_version, task_id)
    REFERENCES task_statements (data_version, task_id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS occupation_ai_score (
  data_version TEXT NOT NULL,
  week VARCHAR(8) NOT NULL,
  soc_code VARCHAR(7) NOT NULL,
  mean NUMERIC(6,2),
  std NUMERIC(6,2),
  ai_augmentation_potential_mean NUMERIC(6,2),
  ai_augmentation_potential_std NUMERIC(6,2),
  human_context_dependency_mean NUMERIC(6,2),
  human_context_dependency_std NUMERIC(6,2),
  physical_world_dependency_mean NUMERIC(6,2),
  physical_world_dependency_std NUMERIC(6,2),
  confidence_mean NUMERIC(6,2),
  confidence_std NUMERIC(6,2),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (data_version, week, soc_code),
  FOREIGN KEY (data_version) REFERENCES data_version(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_occupation_ai_score_mean
  ON occupation_ai_score (data_version, week, mean DESC);

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

-- Tech progress tracking (AI development -> task link -> weekly snapshot)
CREATE TABLE IF NOT EXISTS tech_progress_technology (
  tech_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  domain TEXT,
  synonyms_json JSONB,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  CHECK (status IN ('active', 'inactive'))
);

CREATE TABLE IF NOT EXISTS tech_progress_evidence_source (
  source_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  source_type TEXT NOT NULL,
  base_url TEXT,
  trust_score NUMERIC(4,2),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  CHECK (trust_score IS NULL OR (trust_score >= 0 AND trust_score <= 1))
);

CREATE TABLE IF NOT EXISTS tech_progress_evidence (
  evidence_id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL REFERENCES tech_progress_evidence_source(source_id) ON DELETE CASCADE,
  evidence_date DATE NOT NULL,
  summary TEXT NOT NULL,
  quality_score NUMERIC(4,2) NOT NULL,
  raw_ref TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  CHECK (quality_score >= 0 AND quality_score <= 1)
);

CREATE TABLE IF NOT EXISTS tech_progress_scope_active (
  active_id TEXT PRIMARY KEY,
  week VARCHAR(8) NOT NULL,
  data_version TEXT NOT NULL REFERENCES data_version(id) ON DELETE CASCADE,
  status TEXT NOT NULL DEFAULT 'draft',
  created_by TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  CHECK (status IN ('draft', 'active', 'archived'))
);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_tech_progress_scope_active_week
  ON tech_progress_scope_active (data_version, week)
  WHERE status = 'active';

CREATE TABLE IF NOT EXISTS tech_progress_scope_active_task (
  active_id TEXT NOT NULL REFERENCES tech_progress_scope_active(active_id) ON DELETE CASCADE,
  week VARCHAR(8) NOT NULL,
  data_version TEXT NOT NULL,
  task_id BIGINT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (active_id, task_id),
  FOREIGN KEY (data_version, task_id)
    REFERENCES task_statements (data_version, task_id)
    ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tech_progress_scope_active_task_week
  ON tech_progress_scope_active_task (data_version, week);

CREATE TABLE IF NOT EXISTS tech_progress_task_link (
  id BIGSERIAL PRIMARY KEY,
  week VARCHAR(8) NOT NULL,
  data_version TEXT NOT NULL REFERENCES data_version(id) ON DELETE CASCADE,
  task_id BIGINT NOT NULL,
  tech_id TEXT NOT NULL REFERENCES tech_progress_technology(tech_id) ON DELETE CASCADE,
  link_type TEXT NOT NULL,
  impact_score NUMERIC(4,2) NOT NULL,
  confidence NUMERIC(4,2) NOT NULL,
  evidence_id TEXT NOT NULL REFERENCES tech_progress_evidence(evidence_id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  FOREIGN KEY (data_version, task_id)
    REFERENCES task_statements (data_version, task_id)
    ON DELETE CASCADE,
  CHECK (link_type IN ('enables', 'augments', 'automates', 'replaces', 'requires')),
  CHECK (impact_score >= 0 AND impact_score <= 1),
  CHECK (confidence >= 0 AND confidence <= 1)
);

CREATE UNIQUE INDEX IF NOT EXISTS uniq_tech_progress_task_link_dedupe
  ON tech_progress_task_link (data_version, week, task_id, tech_id, link_type, evidence_id);

CREATE INDEX IF NOT EXISTS idx_tech_progress_task_link_week
  ON tech_progress_task_link (data_version, week);

CREATE TABLE IF NOT EXISTS tech_progress_weekly_snapshot (
  week VARCHAR(8) NOT NULL,
  data_version TEXT NOT NULL REFERENCES data_version(id) ON DELETE CASCADE,
  task_id BIGINT NOT NULL,
  progress_score NUMERIC(4,2) NOT NULL,
  delta NUMERIC(4,2) NOT NULL,
  top_changes_json JSONB,
  evidence_ids_json JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (data_version, week, task_id),
  FOREIGN KEY (data_version, task_id)
    REFERENCES task_statements (data_version, task_id)
    ON DELETE CASCADE,
  CHECK (progress_score >= 0 AND progress_score <= 1),
  CHECK (delta >= -1 AND delta <= 1)
);

CREATE INDEX IF NOT EXISTS idx_tech_progress_weekly_snapshot_week
  ON tech_progress_weekly_snapshot (data_version, week);

CREATE TABLE IF NOT EXISTS tech_progress_llm_task_card (
  data_version TEXT NOT NULL REFERENCES data_version(id) ON DELETE CASCADE,
  week VARCHAR(8) NOT NULL,
  task_id BIGINT NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  payload_json JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (data_version, week, task_id, version),
  FOREIGN KEY (data_version, task_id)
    REFERENCES task_statements (data_version, task_id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tech_progress_llm_weekly_summary (
  data_version TEXT NOT NULL REFERENCES data_version(id) ON DELETE CASCADE,
  week VARCHAR(8) NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  payload_json JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (data_version, week, version)
);

COMMIT;
