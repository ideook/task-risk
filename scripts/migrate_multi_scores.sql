BEGIN;

ALTER TABLE task_ai_score
  ADD COLUMN IF NOT EXISTS ai_substitution_risk NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS ai_augmentation_potential NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS human_context_dependency NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS physical_world_dependency NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS confidence NUMERIC(4,2);

ALTER TABLE task_ai_ensemble
  ADD COLUMN IF NOT EXISTS ai_augmentation_potential_mean NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS ai_augmentation_potential_std NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS ai_augmentation_potential_min NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS ai_augmentation_potential_max NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS human_context_dependency_mean NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS human_context_dependency_std NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS human_context_dependency_min NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS human_context_dependency_max NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS physical_world_dependency_mean NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS physical_world_dependency_std NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS physical_world_dependency_min NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS physical_world_dependency_max NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS confidence_mean NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS confidence_std NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS confidence_min NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS confidence_max NUMERIC(6,2);

ALTER TABLE occupation_ai_score
  ADD COLUMN IF NOT EXISTS ai_augmentation_potential_mean NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS ai_augmentation_potential_std NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS human_context_dependency_mean NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS human_context_dependency_std NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS physical_world_dependency_mean NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS physical_world_dependency_std NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS confidence_mean NUMERIC(6,2),
  ADD COLUMN IF NOT EXISTS confidence_std NUMERIC(6,2);

UPDATE task_ai_score
SET ai_substitution_risk = score
WHERE ai_substitution_risk IS NULL
  AND score IS NOT NULL;

COMMIT;
