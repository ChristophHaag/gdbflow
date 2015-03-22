import argparse
import json
import os
from subprocess import call, PIPE
import pygraphviz as pgv

parser = argparse.ArgumentParser(description='Flow visualization with gdb')
parser.add_argument("-d", "--demo", help="visualize \"simple\" program", action="store_true", dest="demo")
parser.add_argument('program', metavar='program', type=str, help='The program to debug', nargs="?")
parser.add_argument("-q", "--quiet", help="don't show gdb output", dest="quiet", action="store_true")
args = parser.parse_args()
if not args.demo and not args.program:
    print("Error: Need a file name")
    exit(1)

program = ""
if args.demo:
    if not os.access("simple", os.X_OK):
        call(["./compilesimple.sh"])
        print("Compiled simple test program")
    program = "./simple"
else:
    program = args.program

print("Debugging program " + str(program))
if args.quiet:
    print("Running gdb quietly")
    call(["gdb", "-batch-silent", "-q", program, "-x", "gdbflow-gdbscript"], stdout=PIPE, stderr=PIPE)
else:
    print("Running gdb with output")
    call(["gdb", program, "-x", "gdbflow-gdbscript"])

G=pgv.AGraph()
with open("gdbflow-log") as f:
    last = 0
    for index, line in enumerate(f):
        #print(line)
        if not line.strip(): continue
        j = json.loads(line.strip())
        nodename = "Step " + str(index+1) + ":" + \
                   "\nIn line " + str(j["line"]) + " in function " + j["funcname"] + " in file " + j["filename"]
        if "vars" in j and j["vars"]:
            for i in j["vars"]:
                if not i: continue #no vars
                nodename += "\nVariable name: " + str(i["name"])
                nodename += "; Variable type: " + str(i["type"])
                if "value" in i:
                    nodename += "; Variable value: " + str(i["value"])
        G.add_node(nodename)
        G.add_edge(last,nodename)
        last = nodename
    G.write("graph.dot")
    call(["xdot", "graph.dot"])
        #print(str(j))

        #print("Function name: " + j["fn"])