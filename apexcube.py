#!/usr/bin/python
import requests
import xmltodict
import time


skip = ['Email2Alm_I9']
while True:
  try:
    r = requests.get('http://xapexcube.x/cgi-bin/status.xml', timeout=2)
  except:
    print("timeout")
    time.sleep(8)
    continue

  d = xmltodict.parse(r.text, namespaces=True)
  with open('/home/xero/misc/documents/apexcube.txt', 'r+') as out:
    line ='Current Apex Status:\n'+d['status']['date']
    print(line)
    out.write(line+'\n')
    for probe in d['status']['probes']['probe']:
      if probe['name'] in skip or probe['name'].endswith('A') or probe['name'].startswith('Unused'):
        continue
    
      if probe['name'].endswith('W'):
        value = probe['value'] + ' watts'
      else:
        value = probe['value']
      line = '%s: %s' % (probe['name'], value)
      print(line)
      out.write(line+'\n')
    
    for outlet in d['status']['outlets']['outlet']:
      if outlet['name'] in skip or outlet['name'].startswith('VarSpd') or outlet['name'].startswith('Snd') or outlet['name'].startswith('Unused'):
        continue
      
      if outlet['state'] == 'AON':
        state = 'AUTO ON'
      elif outlet['state'] == 'AOF':
        state = 'AUTO OFF'
      else:
        state = outlet['state']
      line = '%s: %s' % (outlet['name'], state)
      print(line)
      out.write(line+'\n')
    out.truncate()
  print()  
  time.sleep(5)
