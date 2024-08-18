WITH fixtures_total AS (

SELECT *
FROM dataset_premiere_league_views.vw_fixtures_home

UNION ALL

SELECT *
FROM dataset_premiere_league_views.vw_fixtures_away

)

SELECT * FROM fixtures_total
