#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, os, sys, csv, re, datetime, ujson as json, unicodedata

def f_conv_date(date):
  try:
    converted = int(time.mktime(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timetuple()))
  except:
    try:
      converted = int(time.mktime(datetime.datetime.strptime(date, '%Y-%m-%d').timetuple())) + (12*60*60)
    except:
      converted = False
      pass
    pass

  return(converted)

def f_zmiana_znakow(s):
  temp = s
  temp = temp.replace('ż', 'z').replace('Ż', 'Z')
  temp = temp.replace('ó', 'o').replace('Ó', 'O')
  temp = temp.replace('ł', 'l').replace('Ł', 'L')
  temp = temp.replace('ć', 'c').replace('Ć', 'C')
  temp = temp.replace('ę', 'e').replace('Ę', 'E')
  temp = temp.replace('ś', 's').replace('Ś', 'S')
  temp = temp.replace('ą', 'a').replace('Ą', 'A')
  temp = temp.replace('ź', 'z').replace('Ź', 'Z')
  temp = temp.replace('ń', 'n').replace('Ń', 'N')
  return(temp)

f = open('dane_stacji.json', 'r')
dane_stacji_raw = json.loads(f.read())
f.close()

dane_stacji = {}
for i in dane_stacji_raw:
  if i['kod_stacji'] in dane_stacji.keys():
    print('duplikacja kodu stacji')
    sys.exit(1)
  dane_stacji[i['kod_stacji']] = i.copy()
  dane_stacji[i['stary_kod_stacji']] = i.copy()

#print(json.dumps(dane_stacji, indent=4))

f_done = open('gotowe_dane_102ba.json', 'w')
f_err = open('gotowe_dane_102bb.json', 'w')

f = open('gotowe_dane_102b_reszta.json', 'r')
tik=0
while True:
 # if tik > 3:
 #   break
  tik+=1
  if tik % 1000000 == 0:
    print(tik)
  try:
    log = json.loads(f.readline())
  except:
    break

  log_2 = {}
  for i in log.keys():
    i_p = i.replace(' ', '_')
    log_2[i_p] = log[i]

  log = log_2.copy()

  if not log['kod_stacji'] in dane_stacji.keys():
    f_err.write(json.dumps(log))
    f_err.write('\n')
  else:
    for k in dane_stacji[log['kod_stacji']].keys():
      if dane_stacji[log['kod_stacji']][k] != None:
        log[k] = dane_stacji[log['kod_stacji']][k]

    for p in ['kod_stanowiska','czas_pomiaru','nr','nazwa_stacji','adres','kod_miedzynarodowy']:
      if p in log.keys():
        del log[p]
    if float(log['wartosc']) < 0.0:
      continue
    f_done.write(json.dumps(log))
    f_done.write('\n')


f.close()
f_done.close()
f_err.close()
