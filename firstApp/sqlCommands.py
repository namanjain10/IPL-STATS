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
