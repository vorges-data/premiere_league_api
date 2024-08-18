SELECT 

  SAFE_CAST(fixture__id AS STRING) AS fixture_id,
  fixture__referee AS soccer_referee,
  fixture__date AS date,
  fixture__status__short AS status_id,
  SAFE_CAST(league__id AS STRING) AS league_id,
  league__season AS league_season,
  league__round AS league_round,
  SAFE_CAST(teams__away__id AS STRING) AS team_id,
  teams__away__name AS team_name,
  teams__away__logo AS team_logo,
  teams__away__winner AS team_winner,
  goals__away AS goals,
  score__fulltime__away AS score_full_time,
  score__halftime__away AS score_first_half,
  CAST(goals__away AS INT64) - CAST(score__halftime__away AS INT64) - CAST(score__extratime__away AS INT64) AS score_second_time,
  score__extratime__away AS score_extratime,
  score__penalty__away AS score_penalty,
  SAFE_CAST(fixture__venue__id AS STRING) AS stadium_id,
  'AWAY' AS away_or_home

FROM dataset_premier_league.past_fixtures

