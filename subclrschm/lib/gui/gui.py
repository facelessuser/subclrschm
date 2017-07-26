# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 22 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.adv
import wx.xrc
import wx.grid

###########################################################################
## Class EditorFrame
###########################################################################

class EditorFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Color Scheme Editor", pos = wx.DefaultPosition, size = wx.Size( 599,417 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_main_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_main_panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		self.m_main_panel.SetMinSize( wx.Size( 500,400 ) )
		
		fgSizer1 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_plist_name_label = wx.StaticText( self.m_main_panel, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_plist_name_label.Wrap( -1 )
		fgSizer2.Add( self.m_plist_name_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_plist_name_textbox = wx.TextCtrl( self.m_main_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer2.Add( self.m_plist_name_textbox, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_plist_uuid_label = wx.StaticText( self.m_main_panel, wx.ID_ANY, u"UUID", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_plist_uuid_label.Wrap( -1 )
		fgSizer2.Add( self.m_plist_uuid_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer10 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer10.AddGrowableCol( 0 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_plist_uuid_textbox = wx.TextCtrl( self.m_main_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer10.Add( self.m_plist_uuid_textbox, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_uuid_button = wx.Button( self.m_main_panel, wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer10.Add( self.m_uuid_button, 0, wx.ALL, 5 )
		
		
		fgSizer2.Add( fgSizer10, 1, wx.EXPAND, 5 )
		
		self.m_search_label = wx.StaticText( self.m_main_panel, wx.ID_ANY, u"Find", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_search_label.Wrap( -1 )
		fgSizer2.Add( self.m_search_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer11 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer11.AddGrowableCol( 0 )
		fgSizer11.SetFlexibleDirection( wx.BOTH )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_search_panel = wx.TextCtrl( self.m_main_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer11.Add( self.m_search_panel, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_button4 = wx.Button( self.m_main_panel, wx.ID_ANY, u"Prev", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer11.Add( self.m_button4, 0, wx.ALL, 5 )
		
		self.m_button5 = wx.Button( self.m_main_panel, wx.ID_ANY, u"Next", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer11.Add( self.m_button5, 0, wx.ALL, 5 )
		
		
		fgSizer2.Add( fgSizer11, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		
		fgSizer1.Add( bSizer3, 1, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_plist_notebook = wx.Notebook( self.m_main_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0|wx.ALWAYS_SHOW_SB|wx.FULL_REPAINT_ON_RESIZE )
		self.m_plist_notebook.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		
		fgSizer1.Add( self.m_plist_notebook, 1, wx.BOTTOM|wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )
		
		
		self.m_main_panel.SetSizer( fgSizer1 )
		self.m_main_panel.Layout()
		fgSizer1.Fit( self.m_main_panel )
		bSizer1.Add( self.m_main_panel, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_menubar = wx.MenuBar( 0 )
		self.m_menu_file = wx.Menu()
		self.m_menuitem_new = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"New", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuitem_new )
		
		self.m_menuitem_open = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuitem_open )
		
		self.m_menuitem_save = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuitem_save )
		
		self.m_menuitem_save_as = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Save As", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuitem_save_as )
		
		self.m_menubar.Append( self.m_menu_file, u"File" ) 
		
		self.m_menu_help = wx.Menu()
		self.m_menuitem_keys = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"Shortcuts", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_help.Append( self.m_menuitem_keys )
		
		self.m_menuitem_about = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_help.Append( self.m_menuitem_about )
		
		self.m_menubar.Append( self.m_menu_help, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar )
		
		self.m_statusbar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_close )
		self.Bind( wx.EVT_KEY_DOWN, self.on_global_key_down )
		self.m_plist_name_textbox.Bind( wx.EVT_KILL_FOCUS, self.on_plist_name_blur )
		self.m_plist_name_textbox.Bind( wx.EVT_TEXT_ENTER, self.on_name_enter )
		self.m_plist_uuid_textbox.Bind( wx.EVT_KILL_FOCUS, self.on_uuid_blur )
		self.m_plist_uuid_textbox.Bind( wx.EVT_TEXT_ENTER, self.on_uuid_enter )
		self.m_uuid_button.Bind( wx.EVT_BUTTON, self.on_uuid_button_click )
		self.m_search_panel.Bind( wx.EVT_TEXT, self.on_find )
		self.m_search_panel.Bind( wx.EVT_TEXT_ENTER, self.on_find_finish )
		self.m_button4.Bind( wx.EVT_BUTTON, self.on_prev_find )
		self.m_button5.Bind( wx.EVT_BUTTON, self.on_next_find )
		self.m_plist_notebook.Bind( wx.EVT_SIZE, self.on_plist_notebook_size )
		self.Bind( wx.EVT_MENU, self.on_create_new, id = self.m_menuitem_new.GetId() )
		self.Bind( wx.EVT_MENU, self.on_open_new, id = self.m_menuitem_open.GetId() )
		self.Bind( wx.EVT_MENU, self.on_save, id = self.m_menuitem_save.GetId() )
		self.Bind( wx.EVT_MENU, self.on_save_as, id = self.m_menuitem_save_as.GetId() )
		self.Bind( wx.EVT_MENU, self.on_shortcuts, id = self.m_menuitem_keys.GetId() )
		self.Bind( wx.EVT_MENU, self.on_about, id = self.m_menuitem_about.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_close( self, event ):
		event.Skip()
	
	def on_global_key_down( self, event ):
		event.Skip()
	
	def on_plist_name_blur( self, event ):
		event.Skip()
	
	def on_name_enter( self, event ):
		event.Skip()
	
	def on_uuid_blur( self, event ):
		event.Skip()
	
	def on_uuid_enter( self, event ):
		event.Skip()
	
	def on_uuid_button_click( self, event ):
		event.Skip()
	
	def on_find( self, event ):
		event.Skip()
	
	def on_find_finish( self, event ):
		event.Skip()
	
	def on_prev_find( self, event ):
		event.Skip()
	
	def on_next_find( self, event ):
		event.Skip()
	
	def on_plist_notebook_size( self, event ):
		event.Skip()
	
	def on_create_new( self, event ):
		event.Skip()
	
	def on_open_new( self, event ):
		event.Skip()
	
	def on_save( self, event ):
		event.Skip()
	
	def on_save_as( self, event ):
		event.Skip()
	
	def on_shortcuts( self, event ):
		event.Skip()
	
	def on_about( self, event ):
		event.Skip()
	

###########################################################################
## Class GlobalSettingsPanel
###########################################################################

class GlobalSettingsPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		fgSizer1 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_button_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_button_panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		
		fgSizer2 = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_row_add = wx.Button( self.m_button_panel, wx.ID_ANY, u"+", wx.DefaultPosition, wx.Size( 30,23 ), wx.BU_EXACTFIT )
		self.m_row_add.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		fgSizer2.Add( self.m_row_add, 0, wx.BOTTOM|wx.LEFT|wx.TOP, 5 )
		
		self.m_row_delete = wx.Button( self.m_button_panel, wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 30,23 ), wx.BU_EXACTFIT )
		self.m_row_delete.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		fgSizer2.Add( self.m_row_delete, 0, wx.BOTTOM|wx.RIGHT|wx.TOP, 5 )
		
		
		self.m_button_panel.SetSizer( fgSizer2 )
		self.m_button_panel.Layout()
		fgSizer2.Fit( self.m_button_panel )
		fgSizer1.Add( self.m_button_panel, 1, wx.EXPAND, 5 )
		
		self.m_plist_grid = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_plist_grid.CreateGrid( 0, 2 )
		self.m_plist_grid.EnableEditing( False )
		self.m_plist_grid.EnableGridLines( False )
		self.m_plist_grid.EnableDragGridSize( False )
		self.m_plist_grid.SetMargins( 0, 0 )
		
		# Columns
		self.m_plist_grid.EnableDragColMove( False )
		self.m_plist_grid.EnableDragColSize( False )
		self.m_plist_grid.SetColLabelSize( 30 )
		self.m_plist_grid.SetColLabelValue( 0, u"Name" )
		self.m_plist_grid.SetColLabelValue( 1, u"Value" )
		self.m_plist_grid.SetColLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_plist_grid.EnableDragRowSize( False )
		self.m_plist_grid.SetRowLabelSize( 0 )
		self.m_plist_grid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_plist_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer1.Add( self.m_plist_grid, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer1 )
		self.Layout()
		
		# Connect Events
		self.m_row_add.Bind( wx.EVT_BUTTON, self.on_row_add_click )
		self.m_row_delete.Bind( wx.EVT_BUTTON, self.on_row_delete_click )
		self.m_plist_grid.Bind( wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.on_edit_cell )
		self.m_plist_grid.Bind( wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.on_grid_label_left_click )
		self.m_plist_grid.Bind( wx.grid.EVT_GRID_SELECT_CELL, self.on_grid_select_cell )
		self.m_plist_grid.Bind( wx.EVT_KEY_DOWN, self.on_grid_key_down )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_row_add_click( self, event ):
		event.Skip()
	
	def on_row_delete_click( self, event ):
		event.Skip()
	
	def on_edit_cell( self, event ):
		event.Skip()
	
	def on_grid_label_left_click( self, event ):
		event.Skip()
	
	def on_grid_select_cell( self, event ):
		event.Skip()
	
	def on_grid_key_down( self, event ):
		event.Skip()
	

###########################################################################
## Class StyleSettingsPanel
###########################################################################

class StyleSettingsPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		fgSizer1 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_button_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_button_panel.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_button_panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		
		fgSizer2 = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_row_up = wx.Button( self.m_button_panel, wx.ID_ANY, u"↑", wx.DefaultPosition, wx.Size( 30,23 ), wx.BU_EXACTFIT )
		self.m_row_up.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		fgSizer2.Add( self.m_row_up, 0, wx.BOTTOM|wx.LEFT|wx.TOP, 5 )
		
		self.m_row_down = wx.Button( self.m_button_panel, wx.ID_ANY, u"↓", wx.DefaultPosition, wx.Size( 30,23 ), wx.BU_EXACTFIT )
		self.m_row_down.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		fgSizer2.Add( self.m_row_down, 0, wx.BOTTOM|wx.RIGHT|wx.TOP, 5 )
		
		self.m_row_add = wx.Button( self.m_button_panel, wx.ID_ANY, u"+", wx.DefaultPosition, wx.Size( 30,23 ), wx.BU_EXACTFIT )
		self.m_row_add.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		fgSizer2.Add( self.m_row_add, 0, wx.ALIGN_RIGHT|wx.BOTTOM|wx.LEFT|wx.TOP, 5 )
		
		self.m_row_delete = wx.Button( self.m_button_panel, wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 30,23 ), wx.BU_EXACTFIT )
		self.m_row_delete.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		fgSizer2.Add( self.m_row_delete, 0, wx.ALIGN_RIGHT|wx.BOTTOM|wx.RIGHT|wx.TOP, 5 )
		
		
		self.m_button_panel.SetSizer( fgSizer2 )
		self.m_button_panel.Layout()
		fgSizer2.Fit( self.m_button_panel )
		fgSizer1.Add( self.m_button_panel, 1, wx.EXPAND, 5 )
		
		self.m_plist_grid = wx.grid.Grid( self, wx.ID_ANY, wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		
		# Grid
		self.m_plist_grid.CreateGrid( 0, 5 )
		self.m_plist_grid.EnableEditing( False )
		self.m_plist_grid.EnableGridLines( False )
		self.m_plist_grid.EnableDragGridSize( False )
		self.m_plist_grid.SetMargins( 0, 0 )
		
		# Columns
		self.m_plist_grid.EnableDragColMove( False )
		self.m_plist_grid.EnableDragColSize( False )
		self.m_plist_grid.SetColLabelSize( 30 )
		self.m_plist_grid.SetColLabelValue( 0, u"Name" )
		self.m_plist_grid.SetColLabelValue( 1, u"Foreground" )
		self.m_plist_grid.SetColLabelValue( 2, u"Background" )
		self.m_plist_grid.SetColLabelValue( 3, u"Font Style" )
		self.m_plist_grid.SetColLabelValue( 4, u"Scope" )
		self.m_plist_grid.SetColLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_plist_grid.AutoSizeRows()
		self.m_plist_grid.EnableDragRowSize( False )
		self.m_plist_grid.SetRowLabelSize( 0 )
		self.m_plist_grid.SetRowLabelAlignment( wx.ALIGN_RIGHT, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_plist_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		self.m_plist_grid.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_plist_grid.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		fgSizer1.Add( self.m_plist_grid, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer1 )
		self.Layout()
		
		# Connect Events
		self.m_row_up.Bind( wx.EVT_BUTTON, self.on_row_up_click )
		self.m_row_down.Bind( wx.EVT_BUTTON, self.on_row_down_click )
		self.m_row_add.Bind( wx.EVT_BUTTON, self.on_row_add_click )
		self.m_row_delete.Bind( wx.EVT_BUTTON, self.on_row_delete_click )
		self.m_plist_grid.Bind( wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.on_edit_cell )
		self.m_plist_grid.Bind( wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.on_grid_label_left_click )
		self.m_plist_grid.Bind( wx.grid.EVT_GRID_SELECT_CELL, self.on_grid_select_cell )
		self.m_plist_grid.Bind( wx.EVT_KEY_DOWN, self.on_grid_key_down )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_row_up_click( self, event ):
		event.Skip()
	
	def on_row_down_click( self, event ):
		event.Skip()
	
	def on_row_add_click( self, event ):
		event.Skip()
	
	def on_row_delete_click( self, event ):
		event.Skip()
	
	def on_edit_cell( self, event ):
		event.Skip()
	
	def on_grid_label_left_click( self, event ):
		event.Skip()
	
	def on_grid_select_cell( self, event ):
		event.Skip()
	
	def on_grid_key_down( self, event ):
		event.Skip()
	

###########################################################################
## Class GlobalSetting
###########################################################################

class GlobalSetting ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Global Setting", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER )
		
		self.SetSizeHints( wx.Size( 500,200 ), wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_global_setting_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 2 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer20 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer20.AddGrowableCol( 1 )
		fgSizer20.SetFlexibleDirection( wx.BOTH )
		fgSizer20.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_name_label = wx.StaticText( self.m_global_setting_panel, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_name_label.Wrap( -1 )
		self.m_name_label.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		
		fgSizer20.Add( self.m_name_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_name_textbox = wx.TextCtrl( self.m_global_setting_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer20.Add( self.m_name_textbox, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer1.Add( fgSizer20, 1, wx.EXPAND, 5 )
		
		self.m_staticline5 = wx.StaticLine( self.m_global_setting_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer1.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer25 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer25.AddGrowableCol( 0 )
		fgSizer25.AddGrowableRow( 0 )
		fgSizer25.SetFlexibleDirection( wx.BOTH )
		fgSizer25.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer21 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer21.AddGrowableCol( 1 )
		fgSizer21.AddGrowableRow( 1 )
		fgSizer21.SetFlexibleDirection( wx.BOTH )
		fgSizer21.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_color_radio = wx.RadioButton( self.m_global_setting_panel, wx.ID_ANY, u"Color", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		fgSizer21.Add( self.m_color_radio, 0, wx.ALL, 5 )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_color_picker = wx.Panel( self.m_global_setting_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 30,-1 ), wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL )
		fgSizer2.Add( self.m_color_picker, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_value_textbox = wx.TextCtrl( self.m_global_setting_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_value_textbox, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer21.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		self.m_text_radio = wx.RadioButton( self.m_global_setting_panel, wx.ID_ANY, u"Text", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer21.Add( self.m_text_radio, 0, wx.ALL, 5 )
		
		self.m_text_textbox = wx.TextCtrl( self.m_global_setting_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB )
		self.m_text_textbox.SetMinSize( wx.Size( -1,30 ) )
		
		fgSizer21.Add( self.m_text_textbox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer25.Add( fgSizer21, 1, wx.EXPAND, 5 )
		
		
		fgSizer1.Add( fgSizer25, 1, wx.EXPAND, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer3.AddGrowableCol( 1 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		
		fgSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_apply_button = wx.Button( self.m_global_setting_panel, wx.ID_ANY, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_apply_button, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		fgSizer1.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		
		self.m_global_setting_panel.SetSizer( fgSizer1 )
		self.m_global_setting_panel.Layout()
		fgSizer1.Fit( self.m_global_setting_panel )
		bSizer1.Add( self.m_global_setting_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_set_color_close )
		self.m_name_textbox.Bind( wx.EVT_KILL_FOCUS, self.on_global_name_blur )
		self.m_color_radio.Bind( wx.EVT_RADIOBUTTON, self.on_radio_click )
		self.m_color_picker.Bind( wx.EVT_LEFT_DOWN, self.on_color_button_click )
		self.m_value_textbox.Bind( wx.EVT_KILL_FOCUS, self.on_color_blur )
		self.m_value_textbox.Bind( wx.EVT_SET_FOCUS, self.on_color_focus )
		self.m_value_textbox.Bind( wx.EVT_TEXT, self.on_color_change )
		self.m_text_radio.Bind( wx.EVT_RADIOBUTTON, self.on_radio_click )
		self.m_apply_button.Bind( wx.EVT_BUTTON, self.on_apply_button_click )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_set_color_close( self, event ):
		event.Skip()
	
	def on_global_name_blur( self, event ):
		event.Skip()
	
	def on_radio_click( self, event ):
		event.Skip()
	
	def on_color_button_click( self, event ):
		event.Skip()
	
	def on_color_blur( self, event ):
		event.Skip()
	
	def on_color_focus( self, event ):
		event.Skip()
	
	def on_color_change( self, event ):
		event.Skip()
	
	
	def on_apply_button_click( self, event ):
		event.Skip()
	

###########################################################################
## Class ColorSetting
###########################################################################

class ColorSetting ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Color Setting", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER )
		
		self.SetSizeHints( wx.Size( 500,200 ), wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_color_setting_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_color_setting_panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		fgSizer23 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer23.AddGrowableCol( 0 )
		fgSizer23.SetFlexibleDirection( wx.BOTH )
		fgSizer23.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer28 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer28.AddGrowableCol( 1 )
		fgSizer28.SetFlexibleDirection( wx.BOTH )
		fgSizer28.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_name_label = wx.StaticText( self.m_color_setting_panel, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_name_label.Wrap( -1 )
		self.m_name_label.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		
		fgSizer28.Add( self.m_name_label, 0, wx.ALL, 5 )
		
		self.m_name_textbox = wx.TextCtrl( self.m_color_setting_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer28.Add( self.m_name_textbox, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_scope_label = wx.StaticText( self.m_color_setting_panel, wx.ID_ANY, u"Scope", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_scope_label.Wrap( -1 )
		self.m_scope_label.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		
		fgSizer28.Add( self.m_scope_label, 0, wx.ALL, 5 )
		
		self.m_scope_textbox = wx.TextCtrl( self.m_color_setting_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer28.Add( self.m_scope_textbox, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer23.Add( fgSizer28, 1, wx.EXPAND, 5 )
		
		self.m_staticline3 = wx.StaticLine( self.m_color_setting_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer23.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		gSizer1 = wx.GridSizer( 0, 3, 0, 0 )
		
		self.m_bold_checkbox = wx.CheckBox( self.m_color_setting_panel, wx.ID_ANY, u"bold", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_bold_checkbox, 0, wx.ALL, 5 )
		
		self.m_italic_checkbox = wx.CheckBox( self.m_color_setting_panel, wx.ID_ANY, u"italic", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_italic_checkbox, 0, wx.ALL, 5 )
		
		self.m_underline_checkbox = wx.CheckBox( self.m_color_setting_panel, wx.ID_ANY, u"underline", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_underline_checkbox, 0, wx.ALL, 5 )
		
		
		fgSizer2.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		
		fgSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		fgSizer23.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 0, 5, 0, 0 )
		fgSizer3.AddGrowableCol( 1 )
		fgSizer3.AddGrowableCol( 3 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_foreground_picker = wx.Panel( self.m_color_setting_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_foreground_button_label = wx.StaticText( self.m_foreground_picker, wx.ID_ANY, u"foreground", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_foreground_button_label.Wrap( -1 )
		bSizer3.Add( self.m_foreground_button_label, 0, wx.ALIGN_CENTER|wx.ALL, 3 )
		
		
		self.m_foreground_picker.SetSizer( bSizer3 )
		self.m_foreground_picker.Layout()
		bSizer3.Fit( self.m_foreground_picker )
		fgSizer3.Add( self.m_foreground_picker, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_foreground_textbox = wx.TextCtrl( self.m_color_setting_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_foreground_textbox, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )
		
		self.m_background_picker = wx.Panel( self.m_color_setting_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_background_button_label = wx.StaticText( self.m_background_picker, wx.ID_ANY, u"background", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_background_button_label.Wrap( -1 )
		bSizer4.Add( self.m_background_button_label, 0, wx.ALL, 3 )
		
		
		self.m_background_picker.SetSizer( bSizer4 )
		self.m_background_picker.Layout()
		bSizer4.Fit( self.m_background_picker )
		fgSizer3.Add( self.m_background_picker, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_background_textbox = wx.TextCtrl( self.m_color_setting_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_background_textbox, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		fgSizer23.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		
		fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_apply_button = wx.Button( self.m_color_setting_panel, wx.ID_ANY, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.m_apply_button, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		fgSizer23.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		
		self.m_color_setting_panel.SetSizer( fgSizer23 )
		self.m_color_setting_panel.Layout()
		fgSizer23.Fit( self.m_color_setting_panel )
		bSizer1.Add( self.m_color_setting_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_set_color_close )
		self.m_foreground_button_label.Bind( wx.EVT_LEFT_DOWN, self.on_foreground_button_click )
		self.m_foreground_textbox.Bind( wx.EVT_KILL_FOCUS, self.on_foreground_blur )
		self.m_foreground_textbox.Bind( wx.EVT_SET_FOCUS, self.on_foreground_focus )
		self.m_foreground_textbox.Bind( wx.EVT_TEXT, self.on_foreground_change )
		self.m_background_button_label.Bind( wx.EVT_LEFT_DOWN, self.on_background_button_click )
		self.m_background_textbox.Bind( wx.EVT_KILL_FOCUS, self.on_background_blur )
		self.m_background_textbox.Bind( wx.EVT_SET_FOCUS, self.on_background_focus )
		self.m_background_textbox.Bind( wx.EVT_TEXT, self.on_background_change )
		self.m_apply_button.Bind( wx.EVT_BUTTON, self.on_apply_button_click )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_set_color_close( self, event ):
		event.Skip()
	
	def on_foreground_button_click( self, event ):
		event.Skip()
	
	def on_foreground_blur( self, event ):
		event.Skip()
	
	def on_foreground_focus( self, event ):
		event.Skip()
	
	def on_foreground_change( self, event ):
		event.Skip()
	
	def on_background_button_click( self, event ):
		event.Skip()
	
	def on_background_blur( self, event ):
		event.Skip()
	
	def on_background_focus( self, event ):
		event.Skip()
	
	def on_background_change( self, event ):
		event.Skip()
	
	def on_apply_button_click( self, event ):
		event.Skip()
	

###########################################################################
## Class AboutDialog
###########################################################################

class AboutDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"About", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_about_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_about_panel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		fgSizer33 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer33.AddGrowableCol( 1 )
		fgSizer33.SetFlexibleDirection( wx.BOTH )
		fgSizer33.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmap = wx.StaticBitmap( self.m_about_panel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 64,64 ), 0 )
		fgSizer33.Add( self.m_bitmap, 0, wx.ALL, 5 )
		
		fgSizer34 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer34.AddGrowableCol( 0 )
		fgSizer34.SetFlexibleDirection( wx.BOTH )
		fgSizer34.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_app_label = wx.StaticText( self.m_about_panel, wx.ID_ANY, u"SubClrSchm", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_app_label.Wrap( -1 )
		self.m_app_label.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		fgSizer34.Add( self.m_app_label, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_version_label = wx.StaticText( self.m_about_panel, wx.ID_ANY, u"Version", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_version_label.Wrap( -1 )
		fgSizer34.Add( self.m_version_label, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_dev_toggle = wx.ToggleButton( self.m_about_panel, wx.ID_ANY, u"Contact >>", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer34.Add( self.m_dev_toggle, 0, wx.ALL, 5 )
		
		self.m_staticline4 = wx.StaticLine( self.m_about_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer34.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_developers_label = wx.StaticText( self.m_about_panel, wx.ID_ANY, u"Dev", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_developers_label.Wrap( -1 )
		self.m_developers_label.Hide()
		
		fgSizer34.Add( self.m_developers_label, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer33.Add( fgSizer34, 1, wx.EXPAND, 5 )
		
		
		fgSizer33.Add( ( 64, 0), 1, wx.EXPAND, 5 )
		
		
		fgSizer33.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		self.m_about_panel.SetSizer( fgSizer33 )
		self.m_about_panel.Layout()
		fgSizer33.Fit( self.m_about_panel )
		bSizer12.Add( self.m_about_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer12 )
		self.Layout()
		bSizer12.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_dev_toggle.Bind( wx.EVT_TOGGLEBUTTON, self.on_toggle )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_toggle( self, event ):
		event.Skip()
