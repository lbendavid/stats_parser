#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import codecs
import re
import argparse
from datetime import datetime
from collections import Counter
import operator
import math

parser = argparse.ArgumentParser()
parser.add_argument("file", help="File name to parse", type=str)
args   = parser.parse_args()

user_system_re        = re.compile(r'System')
user_start_session    = re.compile(r'Network Connect: Session started for user with IP ([.\d]+), hostname (\S+)')
user_end_session      = re.compile(r'Network Connect: Session ended for user with IP ([.\d]+)')
user_session_duration = re.compile(r'Closed connection to TUN-VPN port \d+ after (\d+) seconds')

count     = 0
header    = ['level', 'ip', 'username', 'account', 'date', 'site', 'comment']
max_split = len(header)

user_usage = dict()
pc_usage   = dict()
start_date = datetime.now()
flag       = True

with open(args.file, 'r') as fh:
    for row in fh:
        data = dict(zip(header,row.strip().split(' - ', maxsplit=max_split)))
        
        date_u = data['date']
        if not date_u[:2].isdigit():
            continue
        try:
            date_o = datetime.strptime(date_u, "%Y/%m/%d %H:%M:%S")
            if flag:
                flag = False
                start_date = date_o
        except ValueError:
            continue
        
        user   = data['username'].lower()
        
        # Initialisation de la structure user_usage
        if not user in user_usage:
            user_usage[user]           = dict()
            user_usage[user]['total']  = 0
            user_usage[user]['device'] = Counter()
            user_usage[user]['ip']     = Counter()
        
        # Champs contenant les inforamtions à analyser
        comment = data['comment']
        # Raccourci
        user_u = user_usage[user]
        
        # Début de trace de la session dans la ligne de log
        m = user_start_session.match(comment)
        if m:
            user_u['start'] = date_o
            device = m.group(2).lower()
            
            user_u['ip'][data['ip'][1:-1]] += 1
            user_u['device'][device]       += 1
            user_u['current_device']        = device
        
            continue
        
        if not 'current_device' in user_u:
            continue
        # Fin de trace de la session dans la ligne de log
        m = user_session_duration.match(comment)
        if m:
            # La trace est trunkée, on peut voir des fins de session
            # sans début de session, on ignore ces cas là
            #try:
            #    delta = date_o - user_u['start']
            #except KeyError:
            #    continue
            # session_second = delta.total_seconds()
            session_second = int(m.group(1))
            
            # Initialisation de la partie pc_usage
            if not user_u['current_device'] in pc_usage:
                pc_usage[user_u['current_device']] = dict()
                pc_usage[user_u['current_device']]['total']    = 0
                pc_usage[user_u['current_device']]['users']    = Counter()
            
            pc_usage[user_u['current_device']]['total']       += session_second
            pc_usage[user_u['current_device']]['users'][user] += 1
            
            user_u['total'] += session_second

delta     = date_o - start_date
max_hours = delta.total_seconds()/3600
print("# from {} to {}, elapse: {} - total hours = {:.2f}".format(
    start_date, date_o, delta, max_hours))

i=0
fmt_header    = "{}\t{}\t{}\t{}\t{}"
fmt_data      = "{:d}\t{:.2f}\t{:d}\t{:.2f}\t{:s}"
one_work_week = 3600 # 35 hours/week 
print(fmt_header.format('rank', 'hours', 'nb-users-sharing-pc', 'max-hours', 'pc-name'))

step = 10
histo_pc = Counter()
for k in sorted(pc_usage, key=lambda x: pc_usage[x]['total'], reverse=False):
    hours = pc_usage[k]['total']/one_work_week
    print(fmt_data.format(i, hours, len(pc_usage[k]['users']), max_hours, k))
    rank = math.ceil(hours/step)
    histo_pc[rank] += 1
    i += 1

print("\n\n")
i=0
print(fmt_header.format('rank', 'hours', 'used-devices', 'max-hours', 'user-name'))
for k in sorted(user_usage, key=lambda x: user_usage[x]['total'], reverse=False):
    user_name = re.sub(r'\s+', '_', k)
    print(fmt_data.format(i, user_usage[k]['total']/one_work_week,
                             len(user_usage[k]['device']),
                             max_hours,
                             user_name))
    i += 1

print("\n\n")
print("range-hours\tnumber-of-devices")
for k, v in sorted(histo_pc.items(), key=operator.itemgetter(0)):
    print("{:d}\t{:d}".format(k*step, v))