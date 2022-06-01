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

f = open('gotowe_dane_3a.json', 'r')
fout = open('gotowe_dane_4.json', 'w')
tik=0
while True:
  #if tik > 10:
  #  break
  tik+=1
  if tik % 1000000 == 0:
    print(tik)
  try:
    log = json.loads(f.readline())
  except:
    break
  for p in ['kod_stanowiska','czas_pomiaru','nr','nazwa_stacji','adres','kod_miedzynarodowy']:
    if p in log.keys():
      del log[p]
  fout.write(json.dumps(log))
  fout.write('\n')


f.close()
fout.close()
