-- Expanded mock data (weeks W02-W04)

insert into occupation (onetsoc_code, title, description, status) values
  ('OCC-001', 'Customer Support Analyst', 'Handles inbound customer support operations.', 'defined'),
  ('OCC-002', 'Operations Scheduler', 'Plans staffing and operational schedules.', 'defined'),
  ('OCC-003', 'Back Office Specialist', 'Performs document and data processing tasks.', 'defined');

insert into task_category (task_category_id, name, description) values
  ('CAT-1', 'Customer Support', 'Tasks for customer issue handling.'),
  ('CAT-2', 'Operations Planning', 'Tasks for scheduling and staffing.'),
  ('CAT-3', 'Back Office', 'Tasks for document and data processing.');

insert into task (task_id, task_text, task_category_id, onetsoc_code) values
  ('T1001', 'Categorize incoming support tickets by issue type.', 'CAT-1', 'OCC-001'),
  ('T1002', 'Draft responses to common customer inquiries.', 'CAT-1', 'OCC-001'),
  ('T1003', 'Summarize customer calls and tag next actions.', 'CAT-1', 'OCC-001'),
  ('T2001', 'Create weekly staff schedules based on demand forecasts.', 'CAT-2', 'OCC-002'),
  ('T2002', 'Monitor SLA compliance and adjust staffing.', 'CAT-2', 'OCC-002'),
  ('T2003', 'Forecast ticket volume for upcoming weeks.', 'CAT-2', 'OCC-002'),
  ('T3001', 'Extract fields from incoming documents into system records.', 'CAT-3', 'OCC-003'),
  ('T3002', 'Validate extracted data and resolve exceptions.', 'CAT-3', 'OCC-003');

insert into technology (tech_id, name, domain, synonyms_json, status) values
  ('TECH-LLM-001', 'Customer Support LLM Assistant', 'NLP', '["llm support bot","response drafting"]', 'active'),
  ('TECH-WFM-001', 'Workforce Management Optimizer', 'Operations', '["wfm optimizer","schedule optimizer"]', 'active'),
  ('TECH-VOICE-001', 'Speech-to-Text Engine', 'Speech', '["asr","transcription"]', 'active'),
  ('TECH-OCR-001', 'Document OCR Extractor', 'Document AI', '["ocr","document parsing"]', 'active'),
  ('TECH-RPA-001', 'RPA Workflow Runner', 'Automation', '["robotic process automation"]', 'active'),
  ('TECH-FORE-001', 'Demand Forecasting Model', 'Forecasting', '["volume forecast","time series model"]', 'active');

insert into evidence_source (source_id, name, source_type, base_url, trust_score) values
  ('SRC-REL-001', 'Vendor Release Notes', 'product_release', null, 0.70),
  ('SRC-PAPER-001', 'Research Paper', 'paper', null, 0.85),
  ('SRC-REPO-001', 'Open-source Repo', 'repo', null, 0.60),
  ('SRC-STD-001', 'Industry Standard Update', 'standard', null, 0.75);

insert into evidence (evidence_id, source_id, evidence_date, summary, quality_score, raw_ref) values
  ('E2026W02-001', 'SRC-PAPER-001', '2026-01-06', 'New triage model improves ticket classification accuracy under noisy inputs.', 0.80, 'paper-2026-01-06'),
  ('E2026W02-002', 'SRC-REL-001', '2026-01-07', 'Speech-to-text update reduces word error rate for short calls.', 0.72, 'rel-2026-01-07'),
  ('E2026W03-001', 'SRC-REL-001', '2026-01-13', 'Model update improves response drafting accuracy in customer support workflows.', 0.78, 'rel-2026-01-13'),
  ('E2026W03-002', 'SRC-PAPER-001', '2026-01-15', 'Study shows automatic ticket triage reduces handling time with minimal error.', 0.82, 'paper-2026-01-15'),
  ('E2026W03-003', 'SRC-STD-001', '2026-01-16', 'Standard update clarifies data validation rules for document processing.', 0.70, 'std-2026-01-16'),
  ('E2026W04-001', 'SRC-REPO-001', '2026-01-20', 'Scheduling optimizer adds constraint support for SLA windows.', 0.66, 'repo-2026-01-20'),
  ('E2026W04-002', 'SRC-REL-001', '2026-01-20', 'OCR engine improves table extraction in scanned forms.', 0.74, 'rel-2026-01-20');

insert into task_tech_link (link_id, week, task_id, tech_id, link_type, impact_score, confidence, evidence_id) values
  ('LNK-0001', '2026-W02', 'T1001', 'TECH-LLM-001', 'augments', 0.48, 0.62, 'E2026W02-001'),
  ('LNK-0002', '2026-W02', 'T1003', 'TECH-VOICE-001', 'automates', 0.52, 0.60, 'E2026W02-002'),
  ('LNK-0003', '2026-W03', 'T1002', 'TECH-LLM-001', 'augments', 0.72, 0.75, 'E2026W03-001'),
  ('LNK-0004', '2026-W03', 'T1001', 'TECH-LLM-001', 'automates', 0.64, 0.70, 'E2026W03-002'),
  ('LNK-0005', '2026-W03', 'T3002', 'TECH-RPA-001', 'augments', 0.41, 0.55, 'E2026W03-003'),
  ('LNK-0006', '2026-W04', 'T2001', 'TECH-WFM-001', 'automates', 0.68, 0.72, 'E2026W04-001'),
  ('LNK-0007', '2026-W04', 'T2003', 'TECH-FORE-001', 'augments', 0.58, 0.66, 'E2026W04-001'),
  ('LNK-0008', '2026-W04', 'T3001', 'TECH-OCR-001', 'automates', 0.70, 0.73, 'E2026W04-002');

insert into weekly_snapshot (week, task_id, progress_score, delta, top_changes_json, evidence_ids_json) values
  ('2026-W02', 'T1001', 0.40, 0.05, '["TECH-LLM-001 augments"]', '["E2026W02-001"]'),
  ('2026-W02', 'T1003', 0.45, 0.07, '["TECH-VOICE-001 automates"]', '["E2026W02-002"]'),
  ('2026-W03', 'T1001', 0.58, 0.18, '["TECH-LLM-001 automates"]', '["E2026W03-002"]'),
  ('2026-W03', 'T1002', 0.62, 0.12, '["TECH-LLM-001 augments"]', '["E2026W03-001"]'),
  ('2026-W03', 'T3002', 0.36, 0.04, '["TECH-RPA-001 augments"]', '["E2026W03-003"]'),
  ('2026-W04', 'T2001', 0.60, 0.08, '["TECH-WFM-001 automates"]', '["E2026W04-001"]'),
  ('2026-W04', 'T2003', 0.49, 0.06, '["TECH-FORE-001 augments"]', '["E2026W04-001"]'),
  ('2026-W04', 'T3001', 0.57, 0.09, '["TECH-OCR-001 automates"]', '["E2026W04-002"]');

insert into scope_defined (scope_id, name, scope_type, status, description) values
  ('SCOPE-DEF-001', 'Support and Ops', 'occupation', 'active', 'Defined scope for support and operations roles.'),
  ('SCOPE-DEF-002', 'Back Office', 'occupation', 'active', 'Defined scope for back office roles.');

insert into scope_defined_item (scope_id, item_type, item_id) values
  ('SCOPE-DEF-001', 'occupation', 'OCC-001'),
  ('SCOPE-DEF-001', 'occupation', 'OCC-002'),
  ('SCOPE-DEF-002', 'occupation', 'OCC-003');

insert into scope_active (active_id, week, scope_id, status, created_by) values
  ('ACTIVE-2026W02', '2026-W02', 'SCOPE-DEF-001', 'archived', 'admin'),
  ('ACTIVE-2026W03', '2026-W03', 'SCOPE-DEF-001', 'active', 'admin'),
  ('ACTIVE-2026W04', '2026-W04', 'SCOPE-DEF-002', 'active', 'admin');

insert into scope_active_item (active_id, item_type, item_id) values
  ('ACTIVE-2026W02', 'occupation', 'OCC-001'),
  ('ACTIVE-2026W02', 'occupation', 'OCC-002'),
  ('ACTIVE-2026W03', 'occupation', 'OCC-001'),
  ('ACTIVE-2026W03', 'occupation', 'OCC-002'),
  ('ACTIVE-2026W04', 'occupation', 'OCC-003');

insert into scope_active_task (week, task_id, source_active_id) values
  ('2026-W02', 'T1001', 'ACTIVE-2026W02'),
  ('2026-W02', 'T1002', 'ACTIVE-2026W02'),
  ('2026-W02', 'T1003', 'ACTIVE-2026W02'),
  ('2026-W02', 'T2001', 'ACTIVE-2026W02'),
  ('2026-W02', 'T2002', 'ACTIVE-2026W02'),
  ('2026-W02', 'T2003', 'ACTIVE-2026W02'),
  ('2026-W03', 'T1001', 'ACTIVE-2026W03'),
  ('2026-W03', 'T1002', 'ACTIVE-2026W03'),
  ('2026-W03', 'T1003', 'ACTIVE-2026W03'),
  ('2026-W03', 'T2001', 'ACTIVE-2026W03'),
  ('2026-W03', 'T2002', 'ACTIVE-2026W03'),
  ('2026-W03', 'T2003', 'ACTIVE-2026W03'),
  ('2026-W04', 'T3001', 'ACTIVE-2026W04'),
  ('2026-W04', 'T3002', 'ACTIVE-2026W04');

insert into llm_task_card (week, task_id, version, payload_json) values
  ('2026-W03', 'T1001', 1, '{"week":"2026-W03","task_id":"T1001","task_text":"Categorize incoming support tickets by issue type.","progress_score":0.58,"delta":0.18,"changes":[{"tech":"TECH-LLM-001","link_type":"automates","impact":0.64,"evidence":"E2026W03-002"}],"evidence_briefs":[{"evidence_id":"E2026W03-002","summary":"Automatic ticket triage reduces handling time with minimal error.","date":"2026-01-15"}]}'),
  ('2026-W04', 'T3001', 1, '{"week":"2026-W04","task_id":"T3001","task_text":"Extract fields from incoming documents into system records.","progress_score":0.57,"delta":0.09,"changes":[{"tech":"TECH-OCR-001","link_type":"automates","impact":0.70,"evidence":"E2026W04-002"}],"evidence_briefs":[{"evidence_id":"E2026W04-002","summary":"OCR engine improves table extraction in scanned forms.","date":"2026-01-20"}]}');

insert into llm_weekly_summary (week, version, payload_json) values
  ('2026-W03', 1, '{"week":"2026-W03","top_tasks":[{"task_id":"T1001","delta":0.18},{"task_id":"T1002","delta":0.12}],"notes":["Support ticket triage and response drafting improved most this week."]}'),
  ('2026-W04', 1, '{"week":"2026-W04","top_tasks":[{"task_id":"T3001","delta":0.09},{"task_id":"T2001","delta":0.08}],"notes":["Document extraction and scheduling optimization saw measurable gains."]}');
