CREATE TABLE team_attributes (
ind INTEGER PRIMARY KEY,
team_id INTEGER,
region TEXT,
name TEXT,
abbreviation TEXT,
season INTEGER,
won REAL DEFAULT 0,
lost REAL DEFAULT 0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(0,'Atlanta','Hawks','ATL',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(1,'Boston','Celtics','BOS',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(2,'Charlotte','Bobcats','CHA',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(3,'Chicago','Bulls','CHI',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(4,'Cleveland','Cavaliers','CLE',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(5,'Dallas','Mavericks','DAL',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(6,'Denver','Nuggets','DEN',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(7,'Detroit','Pistons','DET',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(8,'Golden State','Warriors','GSW',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(9,'Houston','Rockets','HOU',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(10,'Indiana','Pacers','IND',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(11,'Los Angeles','Clippers','LAC',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(12,'Los Angeles','Lakers','LAL',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(13,'Memphis','Grizzlies','MEM',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(14,'Miami','Heat','MIA',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(15,'Milwaukee','Bucks','MIL',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(16,'Minnesota','Timberwolves','MIN',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(17,'New Jersey','Nets','NJN',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(18,'New Orleans','Hornets','NOR',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(19,'New York','Knicks','NYK',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(20,'Orlando','Magic','ORL',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(21,'Philadelphia','76ers','PHI',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(22,'Phoenix','Suns','PHO',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(23,'Portland','Trail Blazers','POR',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(24,'Sacramento','Kings','SAC',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(25,'San Antonio','Spurs','SAS',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(26,'Seattle','SuperSonics','SEA',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(27,'Toronto','Raptors','TOR',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(28,'Utah','Jazz','UTA',2008,0.0,0.0);
INSERT INTO "team_attributes" (team_id,region,name,abbreviation,season,won,lost) VALUES(29,'Washington','Wizards','WAS',2008,0.0,0.0);
CREATE TABLE team_stats (
team_id INTEGER,
opponent_team_id INTEGER,
game_id INTEGER,
season INTEGER,
won INTEGER,
minutes INTEGER,
field_goals_made INTEGER,
field_goals_attempted INTEGER,
three_pointers_made INTEGER,
three_pointers_attempted INTEGER,
free_throws_made INTEGER,
free_throws_attempted INTEGER,
offensive_rebounds INTEGER,
defensive_rebounds INTEGER,
assists INTEGER,
turnovers INTEGER,
steals INTEGER,
blocks INTEGER,
personal_fouls INTEGER,
points INTEGER,
opponent_points INTEGER);
