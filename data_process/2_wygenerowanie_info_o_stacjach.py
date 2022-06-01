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

dane_stacji = []
stacja_templatka = {}
nazwy_pol = None

with open('/home/dom/Pobrane/zanieczyszczenia/metadane.csv', 'r') as file:
  reader = csv.reader(file, delimiter = ',')

  templatka_uzupelniona = False
  tik=0
  for fields in reader:
    if not templatka_uzupelniona:
      nazwy_pol = fields
      for f in fields:
        if not f in ['nr']:
          stacja_templatka[f] = None
      templatka_uzupelniona = True
      continue
    temp = stacja_templatka.copy()
    for i in range(len(nazwy_pol)):
      if fields[i] == '':
        continue
      elif nazwy_pol[i] in ['szerokosc', 'dlugosc']: 
        temp[nazwy_pol[i]] = float(fields[i].replace(',', '.'))
      elif nazwy_pol[i] in ['kod_stacji', 'stary_kod_stacji']:
        temp[nazwy_pol[i]] = fields[i]
      elif nazwy_pol[i] in ['nazwa_stacji', 'wojewodztwo', 'miejscowosc']:
        temp[nazwy_pol[i]] = f_zmiana_znakow(s=fields[i].capitalize())
      elif nazwy_pol[i] == 'adres':
        temp[nazwy_pol[i]] = f_zmiana_znakow(s=fields[i].title())
      elif nazwy_pol[i] in ['typ_stacji', 'typ_obszaru', 'rodzaj_stacji', 'kod_miedzynarodowy']:
        temp[nazwy_pol[i]] = f_zmiana_znakow(s=fields[i].lower())
      elif nazwy_pol[i] in ['data_uruchomienia', 'data_zamkniecia']:
        temp[nazwy_pol[i]] = f_conv_date(date=fields[i])
      #else:
      #  print(nazwy_pol[i] + ' => ' + fields[i])

    dane_stacji.append(temp)

f = open('dane_stacji.json', 'w')
f.write(json.dumps(dane_stacji))
f.close()
