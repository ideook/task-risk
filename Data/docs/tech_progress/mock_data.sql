-- Mock data for tech progress tracking

insert into occupation (onetsoc_code, title, description, status) values
  ('OCC-001', 'Customer Support Analyst', 'Handles inbound customer support operations.', 'defined'),
  ('OCC-002', 'Operations Scheduler', 'Plans staffing and operational schedules.', 'defined');

insert into task_category (task_category_id, name, description) values
  ('CAT-1', 'Customer Support', 'Tasks for customer issue handling.'),
  ('CAT-2', 'Operations Planning', 'Tasks for scheduling and staffing.');

insert into task (task_id, task_text, task_category_id, onetsoc_code) values
  ('T1001', 'Categorize incoming support tickets by issue type.', 'CAT-1', 'OCC-001'),
  ('T1002', 'Draft responses to common customer inquiries.', 'CAT-1', 'OCC-001'),
  ('T2001', 'Create weekly staff schedules based on demand forecasts.', 'CAT-2', 'OCC-002'),
  ('T2002', 'Monitor SLA compliance and adjust staffing.', 'CAT-2', 'OCC-002');

insert into technology (tech_id, name, domain, synonyms_json, status) values
  ('TECH-LLM-001', 'Customer Support LLM Assistant', 'NLP', '["llm support bot","response drafting"]', 'active'),
  ('TECH-WFM-001', 'Workforce Management Optimizer', 'Operations', '["wfm optimizer","schedule optimizer"]', 'active'),
  ('TECH-VOICE-001', 'Speech-to-Text Engine', 'Speech', '["asr","transcription"]', 'active');

insert into evidence_source (source_id, name, source_type, base_url, trust_score) values
  ('SRC-REL-001', 'Vendor Release Notes', 'product_release', null, 0.70),
  ('SRC-PAPER-001', 'Research Paper', 'paper', null, 0.85),
  ('SRC-REPO-001', 'Open-source Repo', 'repo', null, 0.60);

insert into evidence (evidence_id, source_id, evidence_date, summary, quality_score, raw_ref) values
  ('E2026W03-001', 'SRC-REL-001', '2026-01-13', 'New model improves response drafting accuracy in customer support workflows.', 0.78, 'rel-2026-01'),
  ('E2026W03-002', 'SRC-PAPER-001', '2026-01-15', 'Study shows automatic ticket triage reduces handling time with minimal error.', 0.82, 'paper-2026-01'),
  ('E2026W04-001', 'SRC-REPO-001', '2026-01-20', 'Open-source scheduling optimizer adds constraint support for SLA windows.', 0.66, 'repo-2026-01');

insert into task_tech_link (link_id, week, task_id, tech_id, link_type, impact_score, confidence, evidence_id) values
  ('LNK-0001', '2026-W03', 'T1002', 'TECH-LLM-001', 'augments', 0.72, 0.75, 'E2026W03-001'),
  ('LNK-0002', '2026-W03', 'T1001', 'TECH-LLM-001', 'automates', 0.64, 0.70, 'E2026W03-002'),
  ('LNK-0003', '2026-W04', 'T2001', 'TECH-WFM-001', 'automates', 0.68, 0.72, 'E2026W04-001'),
  ('LNK-0004', '2026-W04', 'T2002', 'TECH-WFM-001', 'augments', 0.55, 0.65, 'E2026W04-001');

insert into weekly_snapshot (week, task_id, progress_score, delta, top_changes_json, evidence_ids_json) values
  ('2026-W03', 'T1001', 0.58, 0.10, '["TECH-LLM-001 automates"]', '["E2026W03-002"]'),
  ('2026-W03', 'T1002', 0.62, 0.12, '["TECH-LLM-001 augments"]', '["E2026W03-001"]'),
  ('2026-W04', 'T2001', 0.60, 0.08, '["TECH-WFM-001 automates"]', '["E2026W04-001"]'),
  ('2026-W04', 'T2002', 0.52, 0.06, '["TECH-WFM-001 augments"]', '["E2026W04-001"]');

insert into scope_defined (scope_id, name, scope_type, status, description) values
  ('SCOPE-DEF-001', 'Support and Ops', 'occupation', 'active', 'Defined scope for support and operations roles.');

insert into scope_defined_item (scope_id, item_type, item_id) values
  ('SCOPE-DEF-001', 'occupation', 'OCC-001'),
  ('SCOPE-DEF-001', 'occupation', 'OCC-002');

insert into scope_active (active_id, week, scope_id, status, created_by) values
  ('ACTIVE-2026W03', '2026-W03', 'SCOPE-DEF-001', 'active', 'admin');

insert into scope_active_item (active_id, item_type, item_id) values
  ('ACTIVE-2026W03', 'occupation', 'OCC-001'),
  ('ACTIVE-2026W03', 'occupation', 'OCC-002');

insert into scope_active_task (week, task_id, source_active_id) values
  ('2026-W03', 'T1001', 'ACTIVE-2026W03'),
  ('2026-W03', 'T1002', 'ACTIVE-2026W03'),
  ('2026-W03', 'T2001', 'ACTIVE-2026W03'),
  ('2026-W03', 'T2002', 'ACTIVE-2026W03');

insert into llm_task_card (week, task_id, version, payload_json) values
  ('2026-W03', 'T1001', 1, '{"week":"2026-W03","task_id":"T1001","task_text":"Categorize incoming support tickets by issue type.","progress_score":0.58,"delta":0.10,"changes":[{"tech":"TECH-LLM-001","link_type":"automates","impact":0.64,"evidence":"E2026W03-002"}],"evidence_briefs":[{"evidence_id":"E2026W03-002","summary":"Automatic ticket triage reduces handling time with minimal error.","date":"2026-01-15"}]}');

insert into llm_weekly_summary (week, version, payload_json) values
  ('2026-W03', 1, '{"week":"2026-W03","top_tasks":[{"task_id":"T1002","delta":0.12},{"task_id":"T1001","delta":0.10}],"notes":["Support ticket triage and response drafting improved most this week."]}');
