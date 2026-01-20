-- MySQL 8.0.16+ schema (compatible variant)

create table if not exists occupation (
  onetsoc_code varchar(12) primary key,
  title varchar(200) not null,
  description text,
  status varchar(20) not null default 'defined',
  created_at timestamp not null default current_timestamp,
  updated_at timestamp not null default current_timestamp on update current_timestamp,
  check (status in ('defined','inactive'))
);

create table if not exists task_category (
  task_category_id varchar(20) primary key,
  name varchar(200) not null,
  description text
);

create table if not exists task (
  task_id varchar(20) primary key,
  task_text text not null,
  task_category_id varchar(20),
  onetsoc_code varchar(12),
  created_at timestamp not null default current_timestamp,
  updated_at timestamp not null default current_timestamp on update current_timestamp,
  foreign key (task_category_id) references task_category(task_category_id),
  foreign key (onetsoc_code) references occupation(onetsoc_code)
);

create table if not exists technology (
  tech_id varchar(30) primary key,
  name varchar(200) not null,
  domain varchar(100),
  synonyms_json json,
  status varchar(20) not null default 'active',
  created_at timestamp not null default current_timestamp,
  updated_at timestamp not null default current_timestamp on update current_timestamp,
  check (status in ('active','inactive'))
);

create table if not exists evidence_source (
  source_id varchar(30) primary key,
  name varchar(200) not null,
  source_type varchar(30) not null,
  base_url varchar(500),
  trust_score decimal(4,2),
  created_at timestamp not null default current_timestamp,
  check (trust_score is null or (trust_score >= 0 and trust_score <= 1))
);

create table if not exists evidence (
  evidence_id varchar(30) primary key,
  source_id varchar(30) not null,
  evidence_date date not null,
  summary text not null,
  quality_score decimal(4,2) not null,
  raw_ref text,
  created_at timestamp not null default current_timestamp,
  foreign key (source_id) references evidence_source(source_id),
  check (quality_score >= 0 and quality_score <= 1)
);

create table if not exists task_tech_link (
  link_id varchar(30) primary key,
  week varchar(8) not null,
  task_id varchar(20) not null,
  tech_id varchar(30) not null,
  link_type varchar(20) not null,
  impact_score decimal(4,2) not null,
  confidence decimal(4,2) not null,
  evidence_id varchar(30) not null,
  created_at timestamp not null default current_timestamp,
  foreign key (task_id) references task(task_id),
  foreign key (tech_id) references technology(tech_id),
  foreign key (evidence_id) references evidence(evidence_id),
  check (link_type in ('enables','augments','automates','replaces','requires')),
  check (impact_score >= 0 and impact_score <= 1),
  check (confidence >= 0 and confidence <= 1)
);

create table if not exists weekly_snapshot (
  week varchar(8) not null,
  task_id varchar(20) not null,
  progress_score decimal(4,2) not null,
  delta decimal(4,2) not null,
  top_changes_json json,
  evidence_ids_json json,
  created_at timestamp not null default current_timestamp,
  primary key (week, task_id),
  foreign key (task_id) references task(task_id),
  check (progress_score >= 0 and progress_score <= 1),
  check (delta >= -1 and delta <= 1)
);

-- Scope management
create table if not exists scope_defined (
  scope_id varchar(30) primary key,
  name varchar(200) not null,
  scope_type varchar(20) not null,
  status varchar(20) not null default 'active',
  description text,
  created_at timestamp not null default current_timestamp,
  updated_at timestamp not null default current_timestamp on update current_timestamp,
  check (scope_type in ('occupation','task')),
  check (status in ('active','inactive'))
);

create table if not exists scope_defined_item (
  scope_id varchar(30) not null,
  item_type varchar(20) not null,
  item_id varchar(30) not null,
  created_at timestamp not null default current_timestamp,
  primary key (scope_id, item_type, item_id),
  foreign key (scope_id) references scope_defined(scope_id),
  check (item_type in ('occupation','task'))
);

create table if not exists scope_active (
  active_id varchar(30) primary key,
  week varchar(8) not null,
  scope_id varchar(30) not null,
  status varchar(20) not null default 'draft',
  created_by varchar(100),
  created_at timestamp not null default current_timestamp,
  updated_at timestamp not null default current_timestamp on update current_timestamp,
  foreign key (scope_id) references scope_defined(scope_id),
  check (status in ('draft','active','archived'))
);

create table if not exists scope_active_item (
  active_id varchar(30) not null,
  item_type varchar(20) not null,
  item_id varchar(30) not null,
  created_at timestamp not null default current_timestamp,
  primary key (active_id, item_type, item_id),
  foreign key (active_id) references scope_active(active_id),
  check (item_type in ('occupation','task'))
);

create table if not exists scope_active_task (
  week varchar(8) not null,
  task_id varchar(20) not null,
  source_active_id varchar(30) not null,
  created_at timestamp not null default current_timestamp,
  primary key (week, task_id),
  foreign key (task_id) references task(task_id),
  foreign key (source_active_id) references scope_active(active_id)
);

-- LLM delivery
create table if not exists llm_task_card (
  week varchar(8) not null,
  task_id varchar(20) not null,
  version integer not null default 1,
  payload_json json not null,
  created_at timestamp not null default current_timestamp,
  primary key (week, task_id, version),
  foreign key (task_id) references task(task_id)
);

create table if not exists llm_weekly_summary (
  week varchar(8) not null,
  version integer not null default 1,
  payload_json json not null,
  created_at timestamp not null default current_timestamp,
  primary key (week, version)
);

create index idx_task_onet on task(onetsoc_code);
create index idx_task_category on task(task_category_id);
create index idx_link_week on task_tech_link(week);
create index idx_link_task on task_tech_link(task_id);
create index idx_link_tech on task_tech_link(tech_id);
create index idx_evidence_date on evidence(evidence_date);
create index idx_snapshot_week on weekly_snapshot(week);
create index idx_scope_active_week on scope_active(week);
create index idx_scope_active_task_week on scope_active_task(week);
create index idx_llm_task_card_week on llm_task_card(week);

-- Unique link dedupe (no partial index in MySQL)
create unique index ux_link_dedupe
  on task_tech_link(week, task_id, tech_id, link_type, evidence_id);

-- Single active scope per week should be enforced at app layer
