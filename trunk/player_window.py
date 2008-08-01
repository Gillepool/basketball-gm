import sys
import gtk
import pango
import mx.DateTime
import random
import sqlite3

import common

class PlayerWindow:
    def update_player(self, player_id):
        self.player_id = player_id;

        # Roster position
        query = 'SELECT roster_position FROM player_ratings WHERE player_id = ?'
        row = common.DB_CON.execute(query, (self.player_id,)).fetchone()
        self.roster_position = row[0]
        query = 'SELECT COUNT(*), team_id FROM player_attributes WHERE team_id = (SELECT team_id FROM player_attributes WHERE player_id = ?)'
        row = common.DB_CON.execute(query, (self.player_id,)).fetchone()
        self.max_roster_position = row[0]
        self.team_id = row[1]

        # Info
        row = common.DB_CON.execute('SELECT name, position, (SELECT region || " " || name FROM team_attributes WHERE team_id = player_attributes.team_id), height, weight, born_date, born_location, college, draft_year, draft_round, draft_pick, (SELECT region || " " || name FROM team_attributes WHERE team_id = player_attributes.draft_team_id), contract_amount, contract_expiration FROM player_attributes WHERE player_id = ?', (self.player_id,)).fetchone()
        self.player_window.set_title('%s - Player Info' % row[0]);
        [y, m, d] = row[5].split('-', 2)
        height = '%d\'%d"' % (row[3] // 12, row[3] % 12);
        born = mx.DateTime.Date(int(y), int(m), int(d))
        age = mx.DateTime.Age(mx.DateTime.Date(common.SEASON, 1, 1), born).years
        experience = 77 # This should be calculated by how many seasons are recorded, because a player could be injured all year or be out of the leauge
        contract_amount = '$%.2fM' % (row[12]/1000.0)
        self.label_player_window_info.set_markup('<span size="x-large" weight="bold">%s</span>\n<span weight="bold">%s - %s</span>\nHeight: %s\nWeight: %s lbs\nAge: %s\nExperience: %s\nBorn: %s - %s\nCollege: %s\nDraft: %s - Round %s (Pick %s) by the %s\nContract: %s per year through %d' % (row[0], row[1], row[2], height, row[4], age, experience, born.strftime("%B %e, %Y"), row[6], row[7], row[8], row[9], row[10], row[11], contract_amount, row[13]))

        # Ratings
        common.DB_CON.row_factory = sqlite3.Row
        query = 'SELECT overall, height, strength, speed, jumping, endurance, shooting_inside, shooting_layups, shooting_free_throws, shooting_two_pointers, shooting_three_pointers, blocks, steals, dribbling, passing, rebounding, potential FROM player_ratings WHERE player_id = ?'
        row = common.DB_CON.execute(query, (self.player_id,)).fetchone()
        common.DB_CON.row_factory = None
        self.label_rating = {}
        for rating in ('height', 'strength', 'speed', 'jumping', 'endurance', 'shooting_inside', 'shooting_layups', 'shooting_free_throws', 'shooting_two_pointers', 'shooting_three_pointers', 'blocks', 'steals', 'dribbling', 'passing', 'rebounding'):
            self.label_rating[rating] = self.builder.get_object('label_rating_%s' % rating)
            self.label_rating[rating].set_text('%d' % row[rating])
        self.label_player_window_ratings.set_markup('<span size="x-large" weight="bold">Overall Rating: %s</span>\nPotential: %s' % (row['overall'], row['potential']));

        # Stats
        if not self.built['stats']:
            self.build_player_window_stats()
        self.update_player_window_stats()
        # Game Log
        if not self.built['game_log']:
            self.build_player_window_game_log()
        self.update_player_window_game_log()

        self.player_window.show() # Show the dialog
        self.player_window.window.show() # Raise the dialog if it's in the background

    def build_player_window_stats(self):
        common.add_column(self.treeview_player_window_stats, 'Year', 0, True)
        common.add_column(self.treeview_player_window_stats, 'Team', 1, True)
        common.add_column(self.treeview_player_window_stats, 'GP', 2, True)
        common.add_column(self.treeview_player_window_stats, 'GS', 3, True)
        common.add_column(self.treeview_player_window_stats, 'Min', 4, True, True)
        common.add_column(self.treeview_player_window_stats, 'FGM', 5, True, True)
        common.add_column(self.treeview_player_window_stats, 'FGA', 6, True, True)
        common.add_column(self.treeview_player_window_stats, 'FG%', 7, True, True)
        common.add_column(self.treeview_player_window_stats, '3PM', 8, True, True)
        common.add_column(self.treeview_player_window_stats, '3PA', 9, True, True)
        common.add_column(self.treeview_player_window_stats, '3P%', 10, True, True)
        common.add_column(self.treeview_player_window_stats, 'FTM', 11, True, True)
        common.add_column(self.treeview_player_window_stats, 'FTA', 12, True, True)
        common.add_column(self.treeview_player_window_stats, 'FT%', 13, True, True)
        common.add_column(self.treeview_player_window_stats, 'OReb', 14, True, True)
        common.add_column(self.treeview_player_window_stats, 'Dreb', 15, True, True)
        common.add_column(self.treeview_player_window_stats, 'Reb', 16, True, True)
        common.add_column(self.treeview_player_window_stats, 'Ast', 17, True, True)
        common.add_column(self.treeview_player_window_stats, 'TO', 18, True, True)
        common.add_column(self.treeview_player_window_stats, 'Stl', 19, True, True)
        common.add_column(self.treeview_player_window_stats, 'Blk', 20, True, True)
        common.add_column(self.treeview_player_window_stats, 'PF', 21, True, True)
        common.add_column(self.treeview_player_window_stats, 'PPG', 22, True, True)
        self.built['stats'] = True

    def update_player_window_stats(self):
        self.liststore_player_window_stats = gtk.ListStore(int, str, int, int, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float)
        self.treeview_player_window_stats.set_model(self.liststore_player_window_stats)
        query = 'SELECT player_stats.season, (SELECT abbreviation FROM team_attributes WHERE team_id = player_stats.team_id), COUNT(*), SUM(player_stats.starter), AVG(player_stats.minutes), AVG(player_stats.field_goals_made), AVG(player_stats.field_goals_attempted), AVG(100*player_stats.field_goals_made/player_stats.field_goals_attempted), AVG(player_stats.three_pointers_made), AVG(player_stats.three_pointers_attempted), AVG(100*player_stats.three_pointers_made/player_stats.three_pointers_attempted), AVG(player_stats.free_throws_made), AVG(player_stats.free_throws_attempted), AVG(100*player_stats.free_throws_made/player_stats.free_throws_attempted), AVG(player_stats.offensive_rebounds), AVG(player_stats.defensive_rebounds), AVG(player_stats.offensive_rebounds + player_stats.defensive_rebounds), AVG(player_stats.assists), AVG(player_stats.turnovers), AVG(player_stats.steals), AVG(player_stats.blocks), AVG(player_stats.personal_fouls), AVG(player_stats.points) FROM player_attributes, player_stats WHERE player_attributes.player_id = player_stats.player_id AND player_attributes.player_id = ? GROUP BY player_attributes.player_id, player_stats.season, player_stats.team_id ORDER BY player_stats.season DESC'
        for row in common.DB_CON.execute(query, (self.player_id,)):
            stats = []
            for i in range(len(row)):
                # Divide by zero errors
                if row[i] == None:
                    stats.append(0.0)
                else:
                    stats.append(row[i])
            self.liststore_player_window_stats.append(stats)
        self.updated['stats'] = True

    def build_player_window_game_log(self):
        common.add_column(self.treeview_player_window_game_log, 'Game #', 0, True)
        common.add_column(self.treeview_player_window_game_log, 'Team', 1, True)
        common.add_column(self.treeview_player_window_game_log, 'GS', 2, True)
        common.add_column(self.treeview_player_window_game_log, 'Min', 3, True, True)
        common.add_column(self.treeview_player_window_game_log, 'FGM', 4, True, True)
        common.add_column(self.treeview_player_window_game_log, 'FGA', 5, True, True)
        common.add_column(self.treeview_player_window_game_log, 'FG%', 6, True, True)
        common.add_column(self.treeview_player_window_game_log, '3PM', 7, True, True)
        common.add_column(self.treeview_player_window_game_log, '3PA', 8, True, True)
        common.add_column(self.treeview_player_window_game_log, '3P%', 9, True, True)
        common.add_column(self.treeview_player_window_game_log, 'FTM', 10, True, True)
        common.add_column(self.treeview_player_window_game_log, 'FTA', 11, True, True)
        common.add_column(self.treeview_player_window_game_log, 'FT%', 12, True, True)
        common.add_column(self.treeview_player_window_game_log, 'OReb', 13, True, True)
        common.add_column(self.treeview_player_window_game_log, 'Dreb', 14, True, True)
        common.add_column(self.treeview_player_window_game_log, 'Reb', 15, True, True)
        common.add_column(self.treeview_player_window_game_log, 'Ast', 16, True, True)
        common.add_column(self.treeview_player_window_game_log, 'TO', 17, True, True)
        common.add_column(self.treeview_player_window_game_log, 'Stl', 18, True, True)
        common.add_column(self.treeview_player_window_game_log, 'Blk', 19, True, True)
        common.add_column(self.treeview_player_window_game_log, 'PF', 20, True, True)
        common.add_column(self.treeview_player_window_game_log, 'Pts', 21, True, True)
        self.built['game_log'] = True

    def update_player_window_game_log(self):
        self.liststore_player_window_game_log = gtk.ListStore(int, str, int, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float)
        self.treeview_player_window_game_log.set_model(self.liststore_player_window_game_log)
        query = 'SELECT 666, (SELECT abbreviation FROM team_attributes WHERE team_id = player_attributes.team_id), player_stats.starter, player_stats.minutes, player_stats.field_goals_made, player_stats.field_goals_attempted, 100*player_stats.field_goals_made/player_stats.field_goals_attempted, player_stats.three_pointers_made, player_stats.three_pointers_attempted, 100*player_stats.three_pointers_made/player_stats.three_pointers_attempted, player_stats.free_throws_made, player_stats.free_throws_attempted, 100*player_stats.free_throws_made/player_stats.free_throws_attempted, player_stats.offensive_rebounds, player_stats.defensive_rebounds, player_stats.offensive_rebounds + player_stats.defensive_rebounds, player_stats.assists, player_stats.turnovers, player_stats.steals, player_stats.blocks, player_stats.personal_fouls, player_stats.points FROM player_attributes, player_stats WHERE player_attributes.player_id = player_stats.player_id AND player_attributes.player_id = ? AND player_stats.season = ?'
        for row in common.DB_CON.execute(query, (self.player_id, common.SEASON)):
            stats = []
            for i in range(len(row)):
                # Divide by zero errors
                if row[i] == None:
                    stats.append(0.0)
                else:
                    stats.append(row[i])
            self.liststore_player_window_game_log.append(stats)
        self.updated['game_log'] = True

    def on_player_window_close(self, widget, data=None):
        self.player_window.hide()
        return True

    def on_button_previous_clicked(self, button, data=None):
        new_position = self.roster_position - 1
        if new_position < 1:
            new_position = self.max_roster_position
        query = 'SELECT player_ratings.player_id FROM player_attributes, player_ratings WHERE player_attributes.team_id = ? AND player_ratings.roster_position = ? AND player_attributes.player_id = player_ratings.player_id'
        row = common.DB_CON.execute(query, (self.team_id, new_position)).fetchone()
        self.update_player(row[0])

    def on_button_next_clicked(self, button, data=None):
        new_position = self.roster_position + 1
        if new_position > self.max_roster_position:
            new_position = 1
        query = 'SELECT player_ratings.player_id FROM player_attributes, player_ratings WHERE player_attributes.team_id = ? AND player_ratings.roster_position = ? AND player_attributes.player_id = player_ratings.player_id'
        row = common.DB_CON.execute(query, (self.team_id, new_position)).fetchone()
        self.update_player(row[0])

    def on_button_trade_clicked(self, button, data=None):
        print 'trade'

    def on_button_close_clicked(self, button, data=None):
        self.player_window.hide()

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(common.GTKBUILDER_PATH) 
        self.player_window = self.builder.get_object('player_window')
        self.label_player_window_info = self.builder.get_object('label_player_window_info')
        self.label_player_window_ratings = self.builder.get_object('label_player_window_ratings')
        self.treeview_player_window_stats = self.builder.get_object('treeview_player_window_stats')
        self.treeview_player_window_game_log = self.builder.get_object('treeview_player_window_game_log')

        self.built = dict(stats=False, game_log=False)
        self.updated = dict(stats=False, game_log=False)

        self.builder.connect_signals(self)

