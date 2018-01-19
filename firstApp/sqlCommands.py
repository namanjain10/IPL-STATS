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

fifty_season_player = '''SELECT firstApp_season.season_id, hundreds
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


runs_per_match_player = '''SELECT  w.match_id as match_id, match_date, venue_name, city_name, bowler_id, dissimal_type, fielder_id, sum1, balls, round((cast(sum1 as float) / balls * 100),2) as str

    from (select u.match_id, match_date, venue_name, city_name, dissimal_type, bowler_id, fielder_id, sum1
    from
    (select firstApp_match.match_id, sum(batsman_scored) as sum1, match_date, city_name, venue_name
                    from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
                    where striker_id = %d and (innings_id = 1 or innings_id = 2)
                    group by firstApp_match.match_id, match_date, venue_name, city_name) as u left join

    (select d.match_id, dissimal_type, bowler_id, fielder_id
     from firstApp_ball_by_ball
    join (
    select firstApp_match.match_id, sum(batsman_scored) as sum1
    from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
    where striker_id = %d and (innings_id = 1 or innings_id = 2)
    group by firstApp_match.match_id) as d on (firstApp_ball_by_ball.match_id = d.match_id and player_dissimal_id = %d)
    group by d.match_id, dissimal_type, fielder_id, bowler_id
    order by d.match_id) as f
         on u.match_id = f.match_id
                    order by u.match_id) as w
                        join (select match_id , count(*) as balls
                                from (select *
                                    from firstApp_ball_by_ball
                                    where striker_id = %d
                                    except
                                    select *
                                    from firstApp_ball_by_ball
                                    where extra_type = 'wides' or extra_type = 'noballs') as foo
                                    group by match_id) as h on w.match_id = h.match_id
                                    order by w.match_id '''


most_six_season = '''SELECT player_name, striker_id, sixes
    from (select striker_id, count(*) as sixes
    from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
    where batsman_scored = %d and season_id = %d
    group by striker_id
    order by count(*) desc) as d join firstApp_player on player_id = striker_id
    limit 50'''


higest_season = '''SELECT firstApp_match.match_id, match_date, player_id, player_name, highest
    from (select match_id, player_id, player_name, highest
    from (select firstApp_ball_by_ball.match_id, striker_id, sum(batsman_scored) as highest
    from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
    where season_id = %d
    group by firstApp_ball_by_ball.match_id, striker_id) as foo join firstApp_player on player_id = striker_id) as good join firstApp_match on good.match_id = firstApp_match.match_id
    order by highest desc
    limit 50'''


most_runs_season = '''SELECT player_name, striker_id, runs
    from (select striker_id, sum(batsman_scored) as runs
    from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
    where season_id = %d
    group by striker_id
    order by sum(batsman_scored) desc) as d join firstApp_player on player_id = striker_id
    limit 100'''


strike_rate_season = '''SELECT player_name, striker_id, runs, balls, round((cast (runs as float)/balls * 100),2) as str
    from (select striker_id, sum(batsman_scored) as runs, count(*) as balls
          from (select * -- striker_id, sum(batsman_scored) as sum1, count(*) as balls
    from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
    where season_id = %d

        except

        select * -- striker_id, sum(batsman_scored) as sum1, count(*) as balls
    from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
    where season_id = %d and extra_type = 'wides' or extra_type = 'noballs') as foo

    group by striker_id

         ) as d join firstApp_player on player_id = striker_id
    where balls > 50
    order by (cast(runs as float)/balls * 100) desc'''


fifty_season = '''SELECT striker_id, player_name, count(*) as fifty
    from (select firstApp_ball_by_ball.match_id, striker_id, sum(batsman_scored) as sum1
    from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
    where season_id = %d
    group by firstApp_ball_by_ball.match_id, striker_id
    order by sum(batsman_scored) desc) as foo join firstApp_player on player_id = striker_id
    where sum1 >= %d and sum1 < %d
    group by striker_id, player_name
    order by count(*) desc'''


four_innings_season = '''SELECT striker_id, player_name, fours, match_id, match_date
    from (select striker_id, count(*) as fours, firstApp_ball_by_ball.match_id, match_date
    from firstApp_ball_by_ball join firstApp_match on firstApp_match.match_id = firstApp_ball_by_ball.match_id
    where batsman_scored = %d and season_id = %d
    group by firstApp_ball_by_ball.match_id, striker_id
    order by count(*) desc) as foo join firstApp_player on player_id = striker_id
    limit 50'''


partnership = '''SELECT coalesce(fo.match_id, od.match_id) as match_id, coalesce(runs1,0) as runs1 , coalesce(extras1,0) as extras1, coalesce(balls1,0) as balls1, coalesce(runs2,0) as runs2, coalesce(extras2,0) as extras2, coalesce(balls2,0) as balls2
    from (select match_id, sum(batsman_scored) as runs1, count(*) as balls1, sum(extra_runs) as extras1
    from firstApp_ball_by_ball
    where (striker_id = 1 and non_striker_id = 2)
    group by match_id) as fo

    full outer join

    (select match_id, sum(batsman_scored) as runs2, count(*) as balls2, sum(extra_runs) as extras2
    from firstApp_ball_by_ball
    where (striker_id = 2 and non_striker_id = 1)
    group by match_id) as od on fo.match_id= od.match_id;'''


season_bowling = '''SELECT food.season_id, runs, extra, wickets, balls
from (SELECT season_id, sum(runs) as runs, sum(extra) as extra, sum(balls) as balls
    from (select bow.match_id, runs, extra, match_date, balls
    from (select d.match_id, match_date, sum(batsman_scored) as runs, coalesce(sum (extra_runs),0)as extra
    from (select *
      from firstApp_ball_by_ball
      where bowler_id = {0}
      except
      select *
      from firstApp_ball_by_ball
      where bowler_id = {0} and dissimal_type = 'run out'

      union

      select *
        from firstApp_ball_by_ball
        where bowler_id = {0}
        except
      select *
      from firstApp_ball_by_ball
      where (extra_type = 'byes' or extra_type = 'legbyes')) as d join firstApp_match on firstApp_match.match_id = d.match_id

    group by d.match_id, match_date
    order by d.match_id) as bow join (select match_id, count(*) as balls
    from (select *
    from firstApp_ball_by_ball
    where bowler_id = {0}
    except
    select *
     from firstApp_ball_by_ball
     where bowler_id = {0} and (extra_type = 'wides' or extra_type = 'noballs')) as foo
     group by match_id) as ler on bow.match_id = ler.match_id) as d join firstApp_match on firstApp_match.match_id = d.match_id
     group by season_id ) as food left join (select season_id, sum(wickets) as wickets
     from (select match_id, count(*) as wickets
     from firstApp_ball_by_ball
     where bowler_id = {0} and dissimal_type != '' and dissimal_type != 'runout'
     group by match_id)as h join firstApp_match on firstApp_match.match_id = h.match_id
     group by season_id) as hood on food.season_id = hood.season_id'''


per_match_bowling = '''SELECT food.match_id, match_date, runs, extra_runs, coalesce(wickets,0) as wickets, venue_name, city_name
    from (SELECT d.match_id, match_date, coalesce(sum(batsman_scored),0) as runs,coalesce(sum (extra_runs),0) as extra_runs, venue_name, city_name
    from (select *
      from firstApp_ball_by_ball
      where bowler_id = {0}
      except
      select *
      from firstApp_ball_by_ball
      where bowler_id = {0} and dissimal_type = 'run out'

      union

      select *
        from firstApp_ball_by_ball
        where bowler_id = {0}
        except
      select *
      from firstApp_ball_by_ball
      where (extra_type = 'byes' or extra_type = 'legbyes')) as d join firstApp_match on firstApp_match.match_id = d.match_id
    group by d.match_id, match_date, venue_name, city_name
    order by d.match_id) as food left join (select match_id, count(*) as wickets
    from firstApp_ball_by_ball
    where bowler_id = {0} and dissimal_type != '' and dissimal_type != 'runout'
    group by match_id) as hood on food.match_id = hood.match_id
    order by match_date'''
