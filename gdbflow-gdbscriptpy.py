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
    if symbol.is_variable or symbol.is_argument:
      t = None
      try:
        t = str(gdb.types.get_basic_type(symbol.type))
      except Exception as e:
        print (e)
        try:
          t = t = str(gdb.types.deep_items(symbol.type))
        except Exception as e:
          print(e)
          pass
      s = {"name": symbol.print_name, "type": t}
      s["value"] = str(symbol.value(frame))
      s["optimized"] = bool(symbol.value(frame).is_optimized_out)
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