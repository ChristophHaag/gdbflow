import json
gdb.execute("b _start")
gdb.execute("b _exit")
gdb.execute("r")

def localvars(frame):
  try:
    block = gdb.block_for_pc(long(gdb.parse_and_eval('$pc')))
  except: return None
  symbols = []
  for symbol in block:
    s = {"name": symbol.print_name, "type": str(symbol.type)}
    if symbol.is_variable:
      s["value"] = str(symbol.value(frame))
    symbols.append(s)
  return symbols

with open("gdbflow-log", "w") as f:
  while gdb.selected_inferior ().is_valid ():
    #print(str(gdb.selected_inferior ()), gdb.selected_inferior ().is_valid())
    gdb.execute("step")
    #sp = gdb.parse_and_eval("$sp")
    #pc = gdb.parse_and_eval("$pc")
    #line = gdb.find_pc_line(pc)

    #print("line: " + str(line))
    #f.write(str(sp))
    linerep = {}

    frame = gdb.newest_frame ()
    linerep["funcname"] = str(frame.name ())
    sal = frame.find_sal ()
    linerep["line"] = int(sal.line)
    linerep["filename"] = (sal.symtab.filename if sal.symtab else "")
    linerep["vars"] = localvars(frame)

    f.write(json.dumps(linerep))
    f.write("\n")
gdb.execute("quit")
    # Do something with sp.