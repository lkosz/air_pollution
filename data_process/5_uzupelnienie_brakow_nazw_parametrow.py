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

n_par = {
  '123trimetylobenzen': { 'jednostka': 'ug_m3', 'parametr': '123trimetylobenzen' },
  '124trimetylobenzen': { 'jednostka': 'ug_m3', 'parametr': '124trimetylobenzen' },
  '135trimetylobenzen': { 'jednostka': 'ug_m3', 'parametr': '135trimetylobenzen' },
  '13butadien': { 'jednostka': 'ug_m3', 'parametr': '13butadien' },
  '1buten': { 'jednostka': 'ug_m3', 'parametr': '1buten' },
  '1penten': { 'jednostka': 'ug_m3', 'parametr': '1penten' },
  'acetylen': { 'jednostka': 'ug_m3', 'parametr': 'acetylen' },
  'As(PM10)': { 'jednostka': 'ng_m3', 'parametr': 'As_PM10' },
  'BaA(PM10)': { 'jednostka': 'ng_m3', 'parametr': 'BaA_PM10' },
  'BaP(PM10)': { 'jednostka': 'ng_m3', 'parametr': 'BaP_PM10' },
  'BbF(PM10)': { 'jednostka': 'ng_m3', 'parametr': 'BbF_PM10' },
  'BjF(PM10)': { 'jednostka': 'ng_m3', 'parametr': 'BjF_PM10' },
  'BkF(PM10)': { 'jednostka': 'ng_m3', 'parametr': 'BkF_PM10' },
  'C6H6': { 'jednostka': 'ug_m3', 'parametr': 'C6H6' },
  'Ca2+(PM2.5)': { 'jednostka': 'ug_m3', 'parametr': 'Ca2_PM2_5' },
  'Cd(PM10)': { 'jednostka': 'ng_m3', 'parametr': 'Cd_PM10' },
  'cis2buten': { 'jednostka': 'ug_m3', 'parametr': 'cis2buten' },
  'Cl_(PM2.5)': { 'jednostka': 'ug_m3', 'parametr': 'Cl_PM2_5' },
  'Cl': { 'jednostka': 'ug_m3', 'parametr': 'Cl' },
  'CO': { 'jednostka': 'mg_m3', 'parametr': 'CO' },
  'DBahA(PM10)': { 'jednostka': 'ng_m3', 'parametr': 'DBahA_PM10' },
  'DBah(PM10)': { 'jednostka': 'ng_m3', 'parametr': 'DBah_PM10' },
  'EC(PM2.5)': { 'jednostka': 'ug_m3', 'parametr': 'EC_PM2_5' },
  'etan': { 'jednostka': 'ug_m3', 'parametr': 'etan' },
  'etylen': { 'jednostka': 'ug_m3', 'parametr': 'etylen' },
  'etylobenzen': { 'jednostka': 'ug_m3', 'parametr': 'etylobenzen' },
  'formaldehyd': { 'jednostka': 'ug_m3', 'parametr': 'formaldehyd' },
  'Hg(TGM)': { 'jednostka': 'ng_m3', 'parametr': 'Hg_TGM' },
  'ibutan': { 'jednostka': 'ug_m3', 'parametr': 'ibutan' },
  'iheksan': { 'jednostka': 'ug_m3', 'parametr': 'iheksan' },
  'ioktan': { 'jednostka': 'ug_m3', 'parametr': 'ioktan' },
  'ipentan': { 'jednostka': 'ug_m3', 'parametr': 'ipentan' },
  'IP(PM10)': { 'jednostka': 'ng_m3', 'parametr': 'IPPM10' },
  'izopren': { 'jednostka': 'ug_m3', 'parametr': 'izopren' },
  'K+(PM2.5)': { 'jednostka': 'ug_m3', 'parametr': 'K_PM2_5' },
  'Mg2+(PM2.5)': { 'jednostka': 'ug_m3', 'parametr': 'Mg2_PM2_5' },
  'mpksylen': { 'jednostka': 'ug_m3', 'parametr': 'mpksylen' },
  'Na+(PM2.5)': { 'jednostka': 'ug_m3', 'parametr': 'Na_PM2_5' },
  'nbutan': { 'jednostka': 'ug_m3', 'parametr': 'nbutan' },
  'NH4+(PM2.5)': { 'jednostka': 'ug_m3', 'parametr': 'NH4_PM2_5' },
  'nheksan': { 'jednostka': 'ug_m3', 'parametr': 'nheksan' },
  'nheptan': { 'jednostka': 'ug_m3', 'parametr': 'nheptan' },
  'Ni(PM10)': { 'jednostka': 'ng_m3', 'parametr': 'Ni_PM10' },
  'NO': { 'jednostka': 'ug_m3', 'parametr': 'NO' },
  'NO2': { 'jednostka': 'ug_m3', 'parametr': 'NO2' },
  'NO3': { 'jednostka': 'ug_m3', 'parametr': 'NO3' },
  'NO3_(PM2.5)': { 'jednostka': 'ug_m3', 'parametr': 'NO3_PM2_5' },
  'noktan': { 'jednostka': 'ug_m3', 'parametr': 'noktan' },
  'NOx': { 'jednostka': 'ug_m3', 'parametr': 'NOx' },
  'Nox': { 'jednostka': 'ug_m3', 'parametr': 'NOx' },
  'npentan': { 'jednostka': 'ug_m3', 'parametr': 'npentan' },
  'O3': { 'jednostka': 'ug_m3', 'parametr': 'O3' },
  'OC(PM2.5)': { 'jednostka': 'ug_m3', 'parametr': 'OC_PM2_5' },
  'oksylen': { 'jednostka': 'ug_m3', 'parametr': 'oksylen' },
  'Pb(PM10)': { 'jednostka': 'ug_m3', 'parametr': 'Pb_PM10' },
  'PM10': { 'jednostka': 'ug_m3', 'parametr': 'PM10' },
  'PM2.5': { 'jednostka': 'ug_m3', 'parametr': 'PM2_5' },
  'propan': { 'jednostka': 'ug_m3', 'parametr': 'propan' },
  'propen': { 'jednostka': 'ug_m3', 'parametr': 'propen' },
  'SO2': { 'jednostka': 'ug_m3', 'parametr': 'SO2' },
  'SO42_(PM2.5)': { 'jednostka': 'ug_m3', 'parametr': 'SO42_PM2.5' },
  'toluen': { 'jednostka': 'ug_m3', 'parametr': 'toluen' },
  'trans2buten': { 'jednostka': 'ug_m3', 'parametr': 'trans2buten' },
}

poprawki = {
  '2002_SO2_24g.csv': {'par': 'SO2', 'usr': '24g' },
  '2004_NOx_1g.csv': {'par': 'NOx', 'usr': '1g' },
  '2004_SO2_1g.csv': {'par': 'SO2', 'usr': '1g' },
  '2004_SO2_24g.csv': {'par': 'SO2', 'usr': '24g' },
  '2005_C6H6_24g.csv': {'par': 'C6H6', 'usr': '24g' },
  '2005_SO2_24g.csv': {'par': 'SO2', 'usr': '24g' },
  '2006_SO2_24g.csv': {'par': 'SO2', 'usr': '24g' },
  '2007_SO2_24g.csv': {'par': 'SO2', 'usr': '24g' },
  '2008_SO2_24g.csv': {'par': 'SO2', 'usr': '24g' },
  '2009_PM10_24g.csv': {'par': 'PM10', 'usr': '24g' },
  '2009_SO2_24g.csv': {'par': 'SO2', 'usr': '24g' },
  '2010_CO_1g.csv': {'par': 'CO', 'usr': '1g' },
  '2012_NOx_1g.csv': {'par': 'NOx', 'usr': '1g' },
  '2012_O3_1g.csv': {'par': 'O3', 'usr': '1g' },
  '2012_PM10_1g.csv': {'par': 'PM10', 'usr': '1g' },
  '2012_PM2.5_24g.csv': {'par': 'PM2.5', 'usr': '24g' },
  '2013_NOx_1g.csv': {'par': 'NOx', 'usr': '1g' },
}


jednostki = n_par.keys()

f = open('gotowe_dane_103b.json', 'r')
fout = open('gotowe_dane_103ba.json', 'w')
ferr = open('gotowe_dane_103bb.json', 'w')
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

  log['jednostka'] = n_par[poprawki[log['nazwa_pliku']]['par']]['jednostka']
  log['wskaznik'] = n_par[poprawki[log['nazwa_pliku']]['par']]['parametr']
  log['czas_usredniania'] = poprawki[log['nazwa_pliku']]['usr']

  fout.write(json.dumps(log))
  fout.write('\n')


f.close()
fout.close()
ferr.close()
