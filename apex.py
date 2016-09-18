#!/usr/bin/python
import requests
import xmltodict
import time


skip = ['Salt', 'Fan_2_8W', 'Fan_2_8A', 'Fan_2_8', 'Email2Alm_I9']
while True:
  r = requests.get('http://xapex.x/cgi-bin/status.xml')
  d = xmltodict.parse(r.text, namespaces=True)
  with open('/home/xero/misc/documents/apex', 'w+') as out:
    line ='Current Apex Status:\n'+d['status']['date']
    print(line)
    out.write(line+'\n')
    for probe in d['status']['probes']['probe']:
      if probe['name'] in skip or probe['name'].endswith('A'):
        continue
    
      if probe['name'].endswith('W'):
        value = probe['value'] + ' watts'
      else:
        value = probe['value']
      line = '%s: %s' % (probe['name'], value)
      print(line)
      out.write(line+'\n')
    
    for outlet in d['status']['outlets']['outlet']:
      if outlet['name'] in skip or outlet['name'].startswith('VarSpd') or outlet['name'].startswith('Snd'):
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
  print()  
  time.sleep(5)
