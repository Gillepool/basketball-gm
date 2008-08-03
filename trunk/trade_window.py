import gtk
import sqlite3

import common
import random

class TradeWindow:
    def on_trade_window_response(self, dialog, response, *args):
        '''
        This is so the dialog isn't closed on any button except close.
        '''
        if response >= 0:
            self.trade_window.emit_stop_by_name('response')

    def on_treeview_player_row_activated(self, treeview, path, view_column, data=None):
        '''
        Map to the same function in main_window.py
        '''
        self.main_window.on_treeview_player_row_activated(treeview, path, view_column, data)

    def on_button_trade_clear_clicked(self, button, data=None):
        # Reset the offer
        self.offer = [{}, {}]
        for i in range(2):
            model = self.treeview_trade[i].get_model()
            for row in model:
                row[2] = False
        self.update_trade_summary()

    def on_combobox_trade_teams_changed(self, combobox, data=None):
        old = self.other_team_id
        self.other_team_id = combobox.get_active()

        # Can't trade with yourself
        if self.other_team_id == common.PLAYER_TEAM_ID:
            combobox.set_active(old)

        # Update/reset everything if a new team is picked
        if self.other_team_id != old:
            # Reset and update treeview
            for column in self.treeview_trade[1].get_columns():
                self.treeview_trade[1].remove_column(column)
            self.build_roster(self.treeview_trade[1], self.renderer_1)
            self.update_roster(self.treeview_trade[1], self.other_team_id)
            self.renderer_1.disconnect(self.renderer_1_toggled_handle_id)
            self.renderer_1_toggled_handle_id = self.renderer_1.connect('toggled', self.on_player_toggled, self.treeview_trade[1].get_model())

            self.offer[1] = {} # Reset offer for other team only
            self.update_trade_summary()

    def on_player_toggled(self, cell, path, model, data=None):
        model[path][2] = not model[path][2] # Update checkbox

        team_id = model[path][1]
        player_id = model[path][0]
        name = model[path][3]
        if team_id == common.PLAYER_TEAM_ID:
            i = 0
        else:
            i = 1

        if model[path][2]:
            # Check: add player to offer
            contract_amount, = common.DB_CON.execute('SELECT contract_amount FROM player_attributes WHERE player_id = ?', (player_id,)).fetchone()

            self.offer[i][player_id] = [player_id, name, contract_amount]
        else:
            # Uncheck: delete player from offer
            del self.offer[i][player_id]

        self.update_trade_summary()

    def build_roster(self, treeview, renderer_toggle):
        column = gtk.TreeViewColumn('Trade', renderer_toggle)
        column.add_attribute(renderer_toggle, 'active', 2)
        column.set_sort_column_id(2)
        treeview.append_column(column)

        column_info = [['Name', 'Pos', 'Age', 'Rating', 'Potential', 'Contract'],
                       [3,      4,     5,     6,        7,           8],
                       [True,   True,  True,  True,     True,        True],
                       [False,  False, False, False,    False,       False]]
        common.treeview_build(treeview, column_info)

    def update_roster(self, treeview, team_id):
        column_types = [int, int, 'gboolean', str, str, int, int, int, str]
        query = 'SELECT player_attributes.player_id, player_attributes.team_id, 0, player_attributes.name, player_attributes.position, ROUND((julianday("%d-06-01") - julianday(player_attributes.born_date))/365.25), player_ratings.overall, player_ratings.potential, "$" || round(contract_amount/1000.0, 2) || "M thru " || contract_expiration FROM player_attributes, player_ratings WHERE player_attributes.player_id = player_ratings.player_id AND player_attributes.team_id = ? ORDER BY player_ratings.roster_position ASC' % common.SEASON
        query_bindings = (team_id,)
        common.treeview_update(treeview, column_types, query, query_bindings)

    def update_trade_summary(self):
        self.label_trade_summary.set_markup('<b>Trade Summary</b>\n\nSalary Cap: $%.2fM\n' % (common.SALARY_CAP/1000.0))

        payroll_after_trade = [0, 0]
        total = [0, 0]
        over_cap = [False, False]
        ratios = [0, 0]
        names = []
        for team_id in [common.PLAYER_TEAM_ID, self.other_team_id]:
            if team_id == common.PLAYER_TEAM_ID:
                i = 0
                j = 1
            else:
                i = 1
                j = 0
            name, payroll = common.DB_CON.execute('SELECT ta.region || " " || ta.name, sum(pa.contract_amount) FROM team_attributes as ta, player_attributes as pa WHERE pa.team_id = ta.team_id AND ta.team_id = ? AND pa.contract_expiration >= ? AND ta.season = ?', (team_id, common.SEASON, common.SEASON,)).fetchone()
            names.append(name)
            text = '<b>%s</b>\n\nTrade:\n' % name

            total[i] = 0
            for player_id, name, contract_amount in self.offer[i].values():
                text += '%s ($%.2fM)\n' % (name, contract_amount/1000.0)
                total[i] += contract_amount
            text += '$%.2fM total\n\nRecieve:\n' % (total[i]/1000.0)

            total[j] = 0
            for player_id, name, contract_amount in self.offer[j].values():
                text += '%s ($%.2fM)\n' % (name, contract_amount/1000.0)
                total[j] += contract_amount
            text += '$%.2fM total\n\n' % (total[j]/1000.0)
            payroll_after_trade[i] = total[j]+payroll
            text += 'Payroll After Trade: $%.2fM' % (payroll_after_trade[i]/1000.0)

            self.label_trade[i].set_markup(text);

            if payroll_after_trade[i] > common.SALARY_CAP:
                over_cap[i] = True
            if total[i] > 0:
                ratios[i] = int((100.0*total[j])/total[i])
            elif total[j] > 0:
                ratios[i] = float('inf')
            else:
                ratios[i] = 1

        # Update "Propose Trade" button and the salary cap warning
        if (ratios[0] > 125 and over_cap[0] == True) or (ratios[1] > 125 and over_cap[1] == True):
            self.button_trade_propose.set_sensitive(False)
            # Which team is at fault?
            if ratios[0] > 125:
                name = names[0]
                ratio = ratios[0]
            else:
                name = names[1]
                ratio = ratios[1]
            self.label_trade_cap_warning.set_markup('\n<b>The %s are over the salary cap, so the players it receives must have a combined salary less than 125%% of the players it trades.  Currently, that value is %s%%.</b>' % (name, ratio))
        else:
            self.label_trade_cap_warning.set_text('')
            self.button_trade_propose.set_sensitive(True)

    def __init__(self, main_window):
        self.main_window = main_window

        self.builder = gtk.Builder()
        self.builder.add_from_file(common.GTKBUILDER_PATH) 

        self.trade_window = self.builder.get_object('trade_window')
        self.combobox_trade_teams = self.builder.get_object('combobox_trade_teams')
        self.treeview_trade = []
        self.treeview_trade.append(self.builder.get_object('treeview_trade_0'))
        self.treeview_trade.append(self.builder.get_object('treeview_trade_1'))
        self.label_team_name = self.builder.get_object('label_team_name')
        self.label_trade_summary = self.builder.get_object('label_trade_summary')
        self.label_trade = []
        self.label_trade.append(self.builder.get_object('label_trade_0'))
        self.label_trade.append(self.builder.get_object('label_trade_1'))
        self.label_trade_cap_warning = self.builder.get_object('label_trade_cap_warning')
        self.button_trade_propose = self.builder.get_object('button_trade_propose')

        self.builder.connect_signals(self)

        # Fill the combobox with teams
        self.other_team_id = 0
        model = self.combobox_trade_teams.get_model()
        self.combobox_trade_teams.set_model(None)
        model.clear()
        for row in common.DB_CON.execute('SELECT region || " " || name, team_id FROM team_attributes WHERE season = ? ORDER BY team_id ASC', (common.SEASON,)):
            model.append(['%s' % row[0]])
            if row[1] == common.PLAYER_TEAM_ID:
                self.label_team_name.set_text(row[0])
        self.combobox_trade_teams.set_model(model)
        self.combobox_trade_teams.set_active(self.other_team_id)

        # Show the team rosters
        self.renderer_0 = gtk.CellRendererToggle()
        self.renderer_0.set_property('activatable', True)
        self.renderer_1 = gtk.CellRendererToggle()
        self.renderer_1.set_property('activatable', True)
        self.build_roster(self.treeview_trade[0], self.renderer_0)
        self.build_roster(self.treeview_trade[1], self.renderer_1)
        self.update_roster(self.treeview_trade[0], common.PLAYER_TEAM_ID)
        self.update_roster(self.treeview_trade[1], self.other_team_id)
        self.renderer_0.connect('toggled', self.on_player_toggled, self.treeview_trade[0].get_model())
        self.renderer_1_toggled_handle_id = self.renderer_1.connect('toggled', self.on_player_toggled, self.treeview_trade[1].get_model())

        # Initialize offer variable
        self.offer = [{}, {}]

        self.update_trade_summary()

        #self.trade_window.set_transient_for(self.main_window.main_window)

