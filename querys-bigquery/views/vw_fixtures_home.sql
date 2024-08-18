SELECT 

	CAST( fixture__id AS STRING ) as fixture_id,
	fixture__referee as soccer_referee,
	fixture__date as date,
	fixture__status__short as status_id,
	CAST( league__id AS STRING ) as league_id,
	league__season as league_season,
	league__round as league_round, 
	CAST(teams__home__id AS STRING ) AS team_id,
	teams__home__name AS team_name,
	teams__home__logo AS team_logo,
	teams__home__winner AS team_winner,
	goals__home AS goals,
	score__fulltime__home AS score_fulltime,
	score__halftime__home AS score_first_half,
	CAST(goals__home AS INT64) - CAST(score__halftime__home AS INT64) - CAST(score__extratime__home AS INT64) AS score_second_time,
	score__extratime__home AS score_extratime,
	score__penalty__home AS score_penalty,
	CAST(fixture__venue__id AS STRING) AS stadium_id,
	'HOME' AS away_or_home

FROM dataset_premier_league.past_fixtures