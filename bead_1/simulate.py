import sys
import json

sim_data = None # dictionary parsed from json

if len(sys.argv) == 2 :
  try:
    with open(sys.argv[1], 'r') as sim_file : sim_data = json.load(sim_file)
  except:
    print('ERROR:\nError while reading file!')
    exit(1)
else:
  print('ERROR:\nThis program takes ONE argument (file name)\nNumber of arguments provided: {n}'.format(n = len(sys.argv) - 1))
  exit(1)

links    = sim_data['links']                 # links (containing points and capacity)

circuits = sim_data['possible-circuits']     # possible circuits (containing consecutive 'links' [endpoints and switches])

duration = sim_data['simulation']['duration']

demands  = sim_data['simulation']['demands'] # demands

reservations = [] # no reservations at start

def get_link(s, e) :
  for link in links :
    p = link['points']
    if p[0] == s and p[1] == e : return link
  return None

def try_to_reserve(circuit, demand) :
  exists , path = True , []
  for i in range(len(circuit) - 1) :
    link = get_link(circuit[i], circuit[i+1])
    if exists and link != None and link['capacity'] >= demand: path.append(link)
    else : exists = False
  if exists :
    for l in path: l['capacity'] -= demand
  return (exists, path)


for d in demands :
  sp = d['end-points'][0]; ep = d['end-points'][1]
  cs = list(filter(lambda c: c[0] == sp and c[-1] == ep, circuits))
  circuit = cs[0]
  print(d, " >>> ", circuit)
  print(try_to_reserve(circuit, d['demand']))

# TODO free circuits when needed