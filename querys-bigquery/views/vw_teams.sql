SELECT 
  teams__away__id AS team_id,
  teams__away__name AS team_name,
  teams__away__logo AS team_logo
FROM `premier-league-api-431720.dataset_premier_league.past_fixtures`

UNION DISTINCT

SELECT
  teams__home__id,
  teams__home__name,
  teams__home__logo
FROM `premier-league-api-431720.dataset_premier_league.past_fixtures`
