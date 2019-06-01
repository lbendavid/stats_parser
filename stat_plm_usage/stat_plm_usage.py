#!/usr/bin/python3
# -*- coding: utf-8 -*-

from warnings import warn
import csv
import sys
import codecs
import re
from collections import defaultdict
from collections import Counter
from itertools import zip_longest
from operator import itemgetter
from array import array

class defaultlist(list):

   def __setitem__(self, index, value):
      size = len(self)
      if index >= size:
         self.extend(0 for _ in range(size, index + 1))

      list.__setitem__(self, index, value)

csv_file = sys.argv.pop()

is_number = re.compile(r'\d+')
s_plm     = re.compile(r'^.*plm([a-zA-Z0-9]+).*')
is_filter = (
             re.compile(r'OPER', re.I),
             #re.compile('3DEXP', re.I)
             )

scan       = defaultdict(dict)
count      = Counter()
full_count = dict()
channels   = Counter()
header     = tuple()
max        = 0

with codecs.open(csv_file, 'r') as fh: # , 'cp1252' (si fichier pure windows)
    for row in fh:
        
        if is_number.search(row):
            #~ next_loop = True
            #~ for filter in is_filter:
                #~ if not filter.search(row):
                    #~ next_loop = True
                    #~ break
                #~ else:
                    #~ next_loop = False
                    
            #~ if next_loop:
                #~ continue
            if not header:
                continue
            
            #print(row)
            data = dict(zip(header, row.strip().split(';')))
            #print(data)
            try:
                channel = s_plm.sub(r'\1', data['Channel'].lower().split()[1])                
                poste   = data['Poste'].lower()
                domain  = data['Domaine'].lower()
                avion   = data['Avion'].lower()
                annee   = int(data['Année'])
                tsusage = int(data['TSUsage Count'])
                usage   = int(data['Usage Count']) + tsusage
                
            except:
            # Cas des postes inutilisés pour qu'il ne soit pas exclu des stats
            # stat a 0
                avion   = 'EMPTY'
                domain  = 'oper'
                annee   = 2019
                tsusage = 0
                usage   = 0
            
            
            
            # Exclusion
            if not domain == 'oper':
                continue
            if avion == 'batch':
                continue
            
            if poste in full_count:
                pass
            else:
                full_count[poste] = {
                    'years': Counter(),
                    'total': 0,
                    'channel': Counter(),
                }
            
            full_count[poste]['years'][annee]     += usage
            full_count[poste]['channel'][channel] += usage
            full_count[poste]['total']            += usage
            channels[channel]                     += usage
            if full_count[poste]['total'] > max:
                max = full_count[poste]['total']
            
            #print(full_count)
            #print(channel, poste, domain, avion, annee, tsusage, usage)
            #
        else:
            if row.startswith(';'):
                continue
            header = tuple(row.strip().split(';'))
            #print(header)

i=0

channels_list = channels.keys()

print("#poste_range\ttotal\t", "\t".join(channels_list), "#poste\n\"Lancement par poste plm\"")

step = 10
stop = int(max/step)+1
d    = [0 for i in range(0, stop)] #array('i')

for poste, usage in sorted(full_count.items(), key=lambda x: x[1]['total'] , reverse=False):
    fmt = "{}\t{}\t"+"{}\t" * len(channels_list)+"#{}"
    plm = [usage['channel'][channel] for channel in channels_list]
    print(fmt.format(i, usage['total'], *plm, poste))
    total = usage['total']
    if total > 50:
        break
    if total == 0:
        div_slot = 0
        #s= input("Pause [Enter] -->")
        #print(div_slot, poste, usage)
        
    else:
        div_slot = int(total / step)
        if div_slot == 0:
            div_slot = 1

    d[div_slot] += 1

    i += 1

max = 10
print("\n\n#bloc_usage<\tnb_poste\n\"Usage split by step "+str(step)+"\"")
for i, val in enumerate(d):
    #if val == 0:
    #    continue
    print("{}\t{}".format(i*step, val))
    if i > max:
        break
    

