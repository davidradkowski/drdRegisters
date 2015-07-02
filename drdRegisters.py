import sublime, sublime_plugin
from collections import OrderedDict

registers = OrderedDict()

class RegisterCopyCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args ) :
		try:
			reg = args.pop( "character" )
			if( reg ):
				for r in self.view.sel() :
					if( not r.empty() ) :
						registers[ reg ] = self.view.substr( r )
						sublime.status_message( 'Copied to register [ %s ]' % reg )
						break
		except Exception as e :
			print( 'ERR: RegisterCopyCommand: %s' % e )
		return

class RegisterPasteCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args ) :
		try:
			reg = args.pop( 'character' )
			if( reg and reg in registers ):
				self.view.insert( edit, self.view.sel()[ 0 ].begin(), registers[ reg ] )
				sublime.status_message( 'Pasted from register [ %s ]' % reg )
		except Exception as e :
			print( 'ERR: RegisterPasteCommand: %s' % e )
		return

class RegisterListCommand(sublime_plugin.TextCommand):
	def __insert__( self, idx ):
		if( idx >= 0 ):
			k = list( registers.keys() )[ idx ]
			self.view.run_command( 'register_paste', { 'character': k } )
		return
	def run(self, edit, **args ) :
		if( len( registers ) > 0 ):
			rs = list()
			for r in registers:
				rs.append( [ r, registers[ r ] ] )
			try:
				sublime.status_message( 'Pick which register to paste...' )
				sublime.active_window().show_quick_panel( rs, lambda idx: self.__insert__( idx ) )
			except Exception as e :
				print( 'ERR: RegisterListCommand: %s' % e )
		else:
			sublime.status_message( 'Empty registers!' )
		return
		
class RegisterClearAllCommand( sublime_plugin.TextCommand ):
	def run( self, edit, **args ):
		if( len( registers ) > 0 ):
			sublime.status_message( 'Clear all registers' )
			if( sublime.ok_cancel_dialog( 'Do you really want to clear all registers?' ) ):
				registers.clear()
				sublime.status_message( 'All registers cleared!' )
		else:
			sublime.status_message( 'Empty registers!' );
		return

class RegisterSaveCommand( sublime_plugin.TextCommand ):
	def run( self, edit ):
		settings = sublime.load_settings( 'drdRegisters.json' );
		file_name = settings.get( 'file_name', None ) if settings else None
		if( file_name ):
			import pickle
			try:
				pickle.dump( registers, open( file_name, 'wb' ) )
				sublime.status_message( 'Successfully saved registers to {}'.format( file_name ) )
			except Exception as e:
				sublime.status_message( 'Error saving registers to {}: {}'.format( file_name, e ) )
		return
		
class RegisterLoadCommand( sublime_plugin.TextCommand ):
	def run( self, edit ):
		global registers
		settings = sublime.load_settings( 'drdRegisters.json' );
		file_name = settings.get( 'file_name', None ) if settings else None
		if( file_name ):
			import pickle
			try:
				registers = pickle.load( open( file_name, 'rb' ) )
				sublime.status_message( 'Successfully loaded registers from {}'.format( file_name ) )
			except Exception as e:
				sublime.status_message( 'Error loading registers from {}: {}'.format( file_name, e ) )
		return
