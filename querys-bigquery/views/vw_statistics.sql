 WITH stats_aggregated AS (

  SELECT
    SAFE_CAST(fixture AS STRING) AS fixture_id,
    SAFE_CAST(team__id AS STRING) AS team_id,
    team__logo AS team_logo,
    team__name AS team_name,
    ARRAY_AGG(STRUCT(statistics.value, statistics.type)) AS stats_array
  FROM 
    dataset_premier_league.fixturesStatistics
  CROSS JOIN
    UNNEST(statistics) AS statistics
  GROUP BY
    fixture_id,
    team_id,
    team_logo,
    team_name
)

SELECT
  fixture_id,
  team_id,
  team_logo,
  team_name,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Shots on Goal' THEN stat.value ELSE NULL END AS INT64)) AS shots_on_goal,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Shots off Goal' THEN stat.value ELSE NULL END AS INT64)) AS shots_off_goal,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Total Shots' THEN stat.value ELSE NULL END AS INT64)) AS total_shots,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Blocked Shots' THEN stat.value ELSE NULL END AS INT64)) AS blocked_shots,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Shots insidebox' THEN stat.value ELSE NULL END AS INT64)) AS shots_insidebox,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Shots outsidebox' THEN stat.value ELSE NULL END AS INT64)) AS shots_outside,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Fouls' THEN stat.value ELSE NULL END AS INT64)) AS fouls,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Corner Kicks' THEN stat.value ELSE NULL END AS INT64)) AS corner_kicks,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Offsides' THEN stat.value ELSE NULL END AS INT64)) AS offsides,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Ball Possession' THEN REPLACE(stat.value, '%', '') ELSE NULL END AS FLOAT64)) AS ball_possession,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Yellow Cards' THEN stat.value ELSE NULL END AS INT64)) AS yellow_cards,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Red Cards' THEN stat.value ELSE NULL END AS INT64)) AS red_cards,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Goalkeeper Saves' THEN stat.value ELSE NULL END AS INT64)) AS goalkeeper_saves,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Total passes' THEN stat.value ELSE NULL END AS INT64)) AS total_passes,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Passes accurate' THEN stat.value ELSE NULL END AS INT64)) AS passes_accurate,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'Passes %' THEN REPLACE(stat.value, '%', '') ELSE NULL END AS FLOAT64)) AS precision_passes,
  MAX(SAFE_CAST(CASE WHEN stat.type = 'expected_goals' THEN stat.value ELSE NULL END AS FLOAT64)) AS expected_goals

FROM
  stats_aggregated,
  UNNEST(stats_array) AS stat
GROUP BY
  fixture_id,
  team_id,
  team_logo,
  team_name
