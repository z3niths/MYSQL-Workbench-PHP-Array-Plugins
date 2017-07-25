##
# MySQL Workbench - PHP Array From Resultsets 
# Support Workbench Vresion 6.3
# author: z3niths
##

from __future__ import with_statement

# import the wb module
from wb import DefineModule, wbinputs
# import the grt module
import grt
# import the mforms module for GUI stuff
import mforms

import os

from workbench.log import log_error
from workbench.notifications import NotificationCenter

from sql_reformatter import formatter_for_statement_ast
from text_output import TextOutputTab
from run_script import RunScriptForm
from sqlide_catalogman_ext import show_schema_manager
from sqlide_tableman_ext import show_table_inspector

from sqlide_resultset_ext import handleResultsetContextMenu
import sqlide_catalogman_ext
import sqlide_tableman_ext
import sqlide_schematree_ext
import sqlide_import_spatial
import sqlide_power_import_wizard
import sqlide_power_export_wizard

# define this Python module as a GRT module
ModuleInfo = DefineModule(name= "PHPArrayFromResultSet", author= "z3niths", version="1.0")

@ModuleInfo.plugin('wbblog.executePHPArrayFromResultSet', caption='Show PHP Array From Resultsets', input=[wbinputs.currentQueryEditor()], pluginMenu= "SQL/Utilities")
@ModuleInfo.export(grt.INT, grt.classes.db_query_QueryEditor)
def executePHPArrayFromResultSet(editor):
  statement = editor.currentStatement
  if statement:
      rsets = editor.owner.executeScript(statement)
      output = [ '> %s\n' % statement ]
      for idx, rset in enumerate(rsets):
          if len(rsets) > 1:
              output.append('Result set %i' % (idx+1))
          column_name_length = max(len(col.name) for col in rset.columns)
          ok = rset.goToFirstRow()
          while ok:
              output.append('******************** %s. row *********************' % (rset.currentRow + 1))
              output.append('$this->tester->haveInDatabase(Dbs::{REPLACE_TABLENAME}, [')
              for i, column in enumerate(rset.columns):
                  col_name, col_value = column.name.rjust(column_name_length), rset.stringFieldValue(i)
                  output.append('\'%s\' => \'%s\',' % (col_name.strip(), col_value if col_value is not None else 'NULL'))

              output.append(']);,\n')
              ok = rset.nextRow()
          rset.reset_references()            
          if len(rsets) > 1:
            output.append('')
      view = TextOutputTab('\n'.join(output) + '\n')
      
      dock = mforms.fromgrt(editor.resultDockingPoint)
      dock.dock_view(view, '', 0)
      dock.select_view(view)
      view.set_title('Vertical Output')

  return 0


