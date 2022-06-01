from ida_hexrays import *
from ida_dbg import *
from idaapi import *
from idautils import *
from idc import *
from ida_kernwin import *

PLUGIN_NAME = 'kpwd'

class dbg_hooks_t(ida_dbg.DBG_Hooks):
    def __init__(self):
        ida_dbg.DBG_Hooks.__init__(self)
        
    def dbg_suspend_process(self):
        if not get_widget_vdui(get_current_widget()):
            open_pseudocode(get_event_ea(), OPF_NO_WAIT)

class keep_pseudocode(ida_idaapi.plugin_t):

    help = ''
    comment = ''

    wanted_name = PLUGIN_NAME
    wanted_hotkey = 'Ctrl-Shift-K'

    flags = PLUGIN_MOD

    dbg_hooks = None

    def init(self):
        if not init_hexrays_plugin():
            return PLUGIN_SKIP

        print('[+]kpwd load')

        if not self.dbg_hooks:
            self.dbg_hooks = dbg_hooks_t()
            self.dbg_hooks.hook()
            print('[+]kpwd on')

        return PLUGIN_KEEP
        
    def run(self, arg):
        if not self.dbg_hooks:
            self.dbg_hooks = dbg_hooks_t()
            self.dbg_hooks.hook()
            print('[+]kpwd on')
        else:
            self.dbg_hooks.unhook()
            self.dbg_hooks = None
            print('[+]kpwd off')
        
    def term(self):
        if self.dbg_hooks:
            self.dbg_hooks.unhook()
            self.dbg_hooks = None
            print('[+]kpwd off')
        
        print('[+]kpwd unload')

def PLUGIN_ENTRY():
    return keep_pseudocode()