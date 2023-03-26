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

def get_link(s, e):                          # gets link between two points
  for link in links :
    p = link['points']
    if p[0] == s and p[1] == e : return link
  return None

def res_links(circuit, demand):        # tries to reserve a demand between two endpoints
  exists , path = True , []
  for i in range(len(circuit) - 1) :
    link = get_link(circuit[i], circuit[i+1])
    if exists and link != None and link['capacity'] >= demand: path.append(link)
    else : exists = False
  if exists :
    for l in path: l['capacity'] -= demand
  return (exists, path)

def res_circuits(t, event_count):
  for d in demands :
    if d['start-time'] != t : continue

    sp , ep = d['end-points'][0] , d['end-points'][1]
    cs = list(filter(lambda c: c[0] == sp and c[-1] == ep, circuits)) # select possible circuits for d
    circuit = cs[0];                                                  # first possible circuit
    succeeded , reservedLinks = res_links(circuit, d['demand'])       # return values of res_links
    
    if succeeded :
      event_count += 1; print('{c}. igény foglalás: {sp}<->{ep} st:{t} - sikeres'.format(c = event_count, sp = sp, ep = ep, t = t))
      endtime = d['end-time']
      reservations.append({
        'end': endtime,
        'demand': d['demand'],
        'links': reservedLinks
      })
    else:
      event_count += 1; print('{c}. igény foglalás: {sp}<->{ep} st:{t} - sikertelen'.format(c = event_count, sp = sp, ep = ep, t = t))  
  return event_count

def free_circuits(t, event_count):
  tofree = list(filter(lambda r: r['end'] == t,reservations))
  for res in tofree:
    if res['end'] == t :
      for link in res['links'] : link['capacity'] += res['demand']
      reservations.remove(res)
      sp = res['links'][ 0]['points'][0]
      ep = res['links'][-1]['points'][1]
      event_count += 1; print('{c}. igény felszabadítás: {sp}<->{ep} st:{t}'.format(c = event_count, sp = sp, ep = ep, t = t))
  return event_count

event_count = 0 # purely for printing event numbers to stdout

for i in range(duration):
  event_count = res_circuits (i, event_count)
  event_count = free_circuits(i, event_count)