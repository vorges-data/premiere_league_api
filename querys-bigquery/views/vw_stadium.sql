SELECT 
  DISTINCT
  SAFE_CAST(fixture__venue__id AS STRING) AS stadium_id,
  fixture__venue__name AS stadium_name,
  fixture__venue__city AS stadium_city

FROM dataset_premier_league.past_fixtures
WHERE fixture__venue__id IS NOT NULL