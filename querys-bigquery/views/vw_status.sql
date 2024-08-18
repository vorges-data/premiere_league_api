SELECT
  DISTINCT
  fixture__status__short,
  fixture__status__long,

  CASE
    fixture__status__short
  WHEN 'FT' THEN 'Tempo Normal'
  WHEN 'AET' THEN 'Prorrogação'
  WHEN 'PEN' THEN 'Pênaltis'
  ELSE 'Sem Status'
  END AS status_fixtures

FROM dataset_premier_league.past_fixtures