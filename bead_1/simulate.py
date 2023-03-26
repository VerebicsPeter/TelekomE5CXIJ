import sys
import json

sim_data = None # dictionary parsed from json

################################################################################################################################

if len(sys.argv) == 2 :
  try:
    with open(sys.argv[1], 'r') as sim_file : sim_data = json.load(sim_file)
  except:
    print('ERROR:\nError while reading file!')
    exit(1)
else:
  print('ERROR:\nThis program takes ONE argument (file name)\nNumber of arguments provided: {n}'.format(n = len(sys.argv) - 1))
  exit(1)

################################################################################################################################

duration = sim_data['simulation']['duration']

links    = sim_data['links']                 # links (containing points and capacity)

circuits = sim_data['possible-circuits']     # possible circuits (containing consecutive 'links' [endpoints and switches])

demands  = sim_data['simulation']['demands'] # demands

reservations = []                            # no reservations at the start

def get_link(s, e):                         # gets link between two points
  for link in links :
    p = link['points']
    if p[0] == s and p[1] == e : return link
  return None

def try_to_reserve(circuit, demand):        # tries to serve a demand between two endpoints
  exists , path = True , []
  for i in range(len(circuit) - 1) :
    link = get_link(circuit[i], circuit[i+1])
    if exists and link != None and link['capacity'] >= demand: path.append(link)
    else : exists = False
  if exists :
    for l in path: l['capacity'] -= demand
  return (exists, path)

def free_circuits(t):
  tofree = list(filter(lambda r: r['end'] == t,reservations))
  for res in tofree:
    if res['end'] == t :
      for link in res['links'] : link['capacity'] += res['demand']
      reservations.remove(res)
      print('>>> freed:', res['links'], '\n', reservations, '\n')

for i in range(duration) :
  print('Time =', i, '\n')
  
  for d in demands :
    if d['start-time'] != i : continue

    sp , ep = d['end-points'][0] , d['end-points'][1]
    cs = list(filter(lambda c: c[0] == sp and c[-1] == ep, circuits)) # select possible circuits for d
    circuit = cs[0]; print(d, " >>> ", circuit)                       # first possible circuit
    succeeded , reservedLinks = try_to_reserve(circuit, d['demand'])  # values of try_to_reserve
    print(succeeded, ", reserved: ", reservedLinks, '\n')
    
    if succeeded :
      endtime = d['end-time']
      reservations.append({
        'end': endtime,
        'demand': d['demand'],
        'links': reservedLinks
      })
      print('reservation succeeded, reservations: ', reservations, '\n')
  
  free_circuits(i)

# TODO move inner for into own function
# TODO outputs