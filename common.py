import gtk
import sqlite3
import shutil

PLAYER_TEAM_ID = 3

GTKBUILDER_PATH = 'basketball_gm.xml'

shutil.copyfile('database.sqlite', 'temp.sqlite')
DB_FILENAME = 'temp.sqlite'
DB_CON = sqlite3.connect(DB_FILENAME) # This gets changed on file open or close
DB_CON.isolation_level = 'IMMEDIATE'

def treeview_build(treeview, column_info):
    """
    Shortcut function to add columns to a treeview
    """
    for i in range(len(column_info[0])):
        add_column(treeview, column_info[0][i], column_info[1][i], column_info[2][i], column_info[3][i])

def treeview_update(treeview, column_types, query, query_bindings=()):
    """
    Shortcut function to add data to a treeview
    """
    liststore = gtk.ListStore(*column_types)
    treeview.set_model(liststore)
    for row in DB_CON.execute(query, query_bindings):
        values = []
        for i in range(0, len(row)):
            # Divide by zero errors
            if row[i] == None:
                values.append(0.0)
            else:
                values.append(row[i])
        liststore.append(values)

def add_column(treeview, title, column_id, sort=False, truncate_float=False):
    renderer = gtk.CellRendererText()
    column = gtk.TreeViewColumn(title, renderer, text=column_id)
    if sort:
        column.set_sort_column_id(column_id)
    if truncate_float:
        # Truncate floats to 1 decimal place
        column.set_cell_data_func(renderer,
            lambda column, cell, model, iter: cell.set_property('text', '%.1f' % model.get_value(iter, column_id)))
    treeview.append_column(column)