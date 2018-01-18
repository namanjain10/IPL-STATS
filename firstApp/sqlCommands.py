test_str = ''' SELECT match_id, match_date, team_name_id, opponent_team_id, venue_name, city_name, host_country
                from firstApp_match where season_id = %d order by match_date'''

match_bowl_str = '''SELECT h.innings_id, h.bowler_id, player_name, overs, balls, runs, econ, wickets
                from (select q.innings_id, q.bowler_id, player_name, overs, balls, runs, round(cast(runs as float)/(overs*6 + balls)*6,2) as econ

                from (select bowler_id, innings_id, (coalesce(sum(batsman_scored),sum(extra_runs))) as runs

                from (select striker_id, bowler_id, firstApp_ball_by_ball.match_id, innings_id, over_id, ball_id, batsman_scored, extra_type, extra_runs, dissimal_type, fielder_id

                from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
                where firstApp_ball_by_ball.match_id = %d

                except

                select striker_id, bowler_id, firstApp_ball_by_ball.match_id, innings_id, over_id, ball_id, batsman_scored, extra_type, extra_runs, dissimal_type, fielder_id

                from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id

                where firstApp_ball_by_ball.match_id = %d and extra_type = 'legbyes' or extra_type = 'byes') as foo
                group by bowler_id, innings_id) as q join (select bowler_id, player_name, (count(*)/6) as overs, (count(*)%%6) as balls, innings_id

                from (select striker_id, bowler_id, firstApp_ball_by_ball.match_id, innings_id, over_id, ball_id, batsman_scored, extra_type, extra_runs, dissimal_type, fielder_id

                from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
                where firstApp_ball_by_ball.match_id = %d

                except

                select striker_id, bowler_id, firstApp_ball_by_ball.match_id, innings_id, over_id, ball_id, batsman_scored, extra_type, extra_runs, dissimal_type, fielder_id

                from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id

                where firstApp_ball_by_ball.match_id = %d and extra_type = 'wides' or extra_type = 'noballs') as foo join firstApp_player on player_id = bowler_id

                group by bowler_id, innings_id, player_name) as b on (q.bowler_id = b.bowler_id and q.innings_id = b.innings_id)) as h

                left join (select bowler_id, innings_id, count(*) as wickets
                from (select *
                from firstApp_ball_by_ball
                where match_id = %d

                except

                select *
                from firstApp_ball_by_ball
                where match_id = %d and (dissimal_type = 'run out' or dissimal_type = 'runout')) as foo
                where dissimal_type != ''
                group by bowler_id, innings_id ) as r on (r.bowler_id = h.bowler_id and r.innings_id = h.innings_id) '''

player_season = '''SELECT season_id, count(*) as Innings, sum(runs) as Runs, sum(balls)as Balls, sum(fours) as Fours, sum(sixes) as Sixes, round(cast(sum(runs) as float)/sum(balls) * 100, 2) as strike, count(outs) as Outs
    from (select four.match_id, season_id, runs, balls, outs, fours,sixes, str
    from (select foo.match_id, season_id, runs, balls, outs, fours, str
    from (select naman.season_id, naman.match_id, runs, balls, outs, str
    from (select season_id, firstApp_match.match_id, (sum(batsman_scored)) as runs, count(*) as balls, cast(sum(batsman_scored) as float)/count(*) * 100 as str
    from (select * from firstApp_ball_by_ball
            except
    select * from firstApp_ball_by_ball
    where extra_type = 'wides') as firstApp_ball_by_ball join firstApp_match on firstApp_ball_by_ball.match_id = firstApp_match.match_id
    where striker_id = %d
    group by season_id, firstApp_match.match_id
    order by season_id desc) as naman left join (select season_id, firstApp_match.match_id, count(*) as outs
    from firstApp_ball_by_ball join firstApp_match on firstApp_ball_by_ball.match_id = firstApp_match.match_id
    where striker_id = %d and player_dissimal_id = %d
    group by season_id, firstApp_match.match_id
    order by season_id desc) as jain on naman.match_id = jain.match_id) as foo left join
    (select match_id, count(*) as fours
    from firstApp_ball_by_ball
    where striker_id = %d and batsman_scored = 4
    group by match_id) as ood on foo.match_id = ood.match_id) as four left join (select match_id, count(*) as sixes
    from firstApp_ball_by_ball
    where striker_id = %d and batsman_scored = 6
    group by match_id) as sixes on four.match_id = sixes.match_id)as total
    group by season_id'''

fifty_season = '''SELECT firstApp_season.season_id, hundreds
    from firstApp_season left join (select season_id, count(*) as hundreds
    from (select match_id, sum(batsman_scored) as runs
    from firstApp_ball_by_ball
    where striker_id = %d
    group by match_id
    having sum(batsman_scored) between %d and %d)as foo join firstApp_match on foo.match_id = firstApp_match.match_id
    group by season_id) as food on food.season_id = firstApp_season.season_id'''

highest_season = '''SELECT firstApp_season.season_id, highest
    from firstApp_season left join (select season_id, max(runs) as highest
    from (select match_id, sum(batsman_scored) as runs
    from firstApp_ball_by_ball
    where striker_id = %d
    group by match_id)as foo join firstApp_match on foo.match_id = firstApp_match.match_id
    group by season_id) as food on food.season_id = firstApp_season.season_id'''

wins = '''SELECT firstApp_season.season_id, wins
    from firstApp_season left join (SELECT season_id, count(*) as wins
    from firstApp_match
    where (team_name_id = {0} or opponent_team_id = {0}) and match_winner_id = {0}
    group by season_id) as foo on firstApp_season.season_id = foo.season_id'''

losses = '''SELECT firstApp_season.season_id, losses
    from firstApp_season left join (SELECT season_id, count(*) as losses
    from firstApp_match
    where (team_name_id = {0} or opponent_team_id = {0}) and match_winner_id != {0}
    group by season_id) as foo on firstApp_season.season_id = foo.season_id'''

nr = '''SELECT firstApp_season.season_id, nr
    from firstApp_season left join (SELECT season_id, count(*) as nr
    from firstApp_match
    where (team_name_id = {0} or opponent_team_id = {0}) and is_result = 0
    group by season_id) as foo on firstApp_season.season_id = foo.season_id'''
