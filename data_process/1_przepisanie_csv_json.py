#!/usr/bin/env python

import time, os, sys, csv, re, datetime, ujson as json

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

f = open('gotowe_dane100.json', 'w')
for file in sorted(os.listdir('/home/dom/Pobrane/zanieczyszczenia/dane_csv_raw')):
  print(file)
  dane = {
    'kod stanowiska': None,
    'czas pomiaru': None,
    'kod stacji': None,
    'nr': None,
    'czas usredniania': None,
    'wskaznik': None,
    'jednostka': None,
    'nazwa_pliku': file,
    'dane': []
  }
  with open('/home/dom/Pobrane/zanieczyszczenia/dane_csv_raw/' + file, 'r') as file:
    reader = csv.reader(file, delimiter = ',')

    for fields in reader:
      out = f_conv_date(date=fields[0])
      if out != False:
        fields[0] = out
        dane['dane'].append(fields)
      elif fields[0] == 'Kod stanowiska':
        dane['kod stanowiska'] = fields
      elif fields[0] == 'Czas pomiaru':
        dane['czas pomiaru'] = fields
      elif fields[0] == 'Kod stacji' or (fields[0] == '' and (fields[1].startswith('Ds') or fields[1].startswith('Mp') or fields[1].startswith('Wm') or fields[1].startswith('Lb') or fields[1].startswith('Kp'))):
        dane['kod stacji'] = fields
      elif fields[0] == 'Nr' or fields[0] == 'Numer' or (fields[0] == '' and fields[1] == '1'):
        dane['nr'] = fields
      elif fields[0] == 'Czas u?redniania' or (fields[0] == '' and fields[1] in ['24g', '1g']):
        dane['czas usredniania'] = fields
      elif fields[0] == 'Wska?nik' or (fields[0] == '' and fields[1] in ['123trimetylobenzen', 'As(PM10)', 'BaA(PM10)', 'BaP(PM10)', 'BbF(PM10)', 'BjF(PM10)', 'BkF(PM10)', 'C6H6', 'Ca2+(PM2.5)', 'Cd(PM10)', 'Cl', 'CO', 'DBahA(PM10)', 'DBah(PM10)', 'EC(PM2.5)', 'formaldehyd', 'Hg(TGM)', 'IP(PM10)', 'Jest', 'K+(PM2.5)', 'Mg2+(PM2.5)', 'Na+(PM2.5)', 'NH4+(PM2.5)', 'Ni(PM10)', 'NO', 'NO2', 'NO3', 'Nox', 'NOx', 'O3', 'OC(PM2.5)', 'Pb(PM10)', 'PM10', 'PM2.5', 'SO2', 'SO42_(PM2.5)']):
        dane['wskaznik'] = fields
      elif fields[0] == 'Jednostka'  or (fields[0] == '' and fields[1] in ['ng/m3', 'ug/m3', 'mg/m3']):
        dane['jednostka'] = fields
      else:
        print(fields)

# sprawdzenie czy dane są odpowiedniej długości
#  dlug = None
#  for k in dane.keys():
#    if k == 'dane':
#      continue
#    if dane[k] != None:
#      if dlug == None:
#        dlug = len(dane[k])
#      else:
#        if dlug != len(dane[k]):
#          print(k)
#          sys.exit(1)
#  for d in dane['dane']:
#    if len(d) != dlug:
#      print(d)
#      sys.exit(1)
#  if dane['kod stacji'] == None:
#    print('kod stacji = none!!!!!!!!!!!!!!')
#    sys.exit(1)



  for stacja in range(len(dane['kod stacji'])):
    if stacja == 0:
      continue
    log_wzor = {
      'kod stanowiska': None,
      'czas pomiaru': None,
      'kod stacji': None,
      'nr': None,
      'czas usredniania': None,
      'wskaznik': None,
      'jednostka': None,
      'data': None,
      'wartosc': None
    }
    for parametr in dane.keys():
      if parametr in ['dane', 'nazwa_pliku']:
        continue
      if dane[parametr] != None:
        log_wzor[parametr] = dane[parametr][stacja]

    for pomiar in dane['dane']:
      if pomiar[stacja] == '':
        continue
      else:
        log_pomiar = log_wzor.copy()
        log_pomiar['data'] = int(pomiar[0])
        log_pomiar['wartosc'] = float(str(pomiar[stacja]).replace(',', '.'))
        log_pomiar['nazwa_pliku'] = dane['nazwa_pliku']
        f.write(json.dumps(log_pomiar))
        f.write('\n')


f.close()
