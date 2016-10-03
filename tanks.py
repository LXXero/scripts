#!/usr/bin/python
import threading
import requests
import queue
import xmltodict
import time
import pyautogui


def apexpoller(c):
  threading.Timer(5, apexpoller, [c]).start()
  try:
    r = requests.get(c['url'], timeout=2)
  except:
    print('timeout\n')
    return

  d = xmltodict.parse(r.text, namespaces=True)
  with open(c['file'], 'r+') as out:
    line ='Current Apex Status:\n'+d['status']['date']
    print(line)
    out.write(line+'\n')
    for probe in d['status']['probes']['probe']:
      if probe['name'] in c['skip'] or probe['name'].endswith('A') or probe['name'].startswith(tuple(c['startswith'])):
        continue
    
      if probe['name'].endswith('W'):
        value = probe['value'] + ' watts'
      else:
        value = probe['value']
      line = '%s: %s' % (probe['name'], value)
      print(line)
      out.write(line+'\n')
    
    for outlet in d['status']['outlets']['outlet']:
      if outlet['name'] in c['skip'] or outlet['name'].startswith(tuple(c['startswith'])) or outlet['name'].endswith(tuple(c['endswith'])):
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


import sys


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stopit = threading.Event()

    def stopit(self):
        self._stopit.set()

    def stopped(self):
        return self._stopit.isSet()

class count_down(StoppableThread):
  def __init__(self, head = '(', seconds = 120, foot = ')', file = '/home/xero/misc/documents/scene.txt', eol = '\033[0K\r'):
    StoppableThread.__init__(self)
    self.head = head
    self.seconds = seconds
    self.foot = foot
    self.file = file
    self.eol = eol
    print( "thread init", file=sys.stderr )
  def run(self):
    for t in range(self.seconds, -1, -1):
      sf = self.head + "{:d}:{:02d}".format(*divmod(t, 60)) + self.foot
      print(sf, end=self.eol)
      with open(self.file, 'r+') as out:
        out.write(sf+'\n')
        out.truncate()
      if self.stopped():
        break
      time.sleep(1)

def stoptimer():
  try:
    timer.stopit()
  except:
    pass 

def timeralive():
  while True:
    if timer.is_alive() == True:
      timer.join()
    else:
      break


def cmdinput():
  while True:
    #print("timer is %s" % timer)
    input_cmd = input("Enter Command: ")
    #print ("Command Received " + input_cmd)
    if input_cmd == 'next':
      stoptimer()
    if input_cmd == 'scene1':
      scene1()
    if input_cmd == 'scene2':
      scene2()
    if input_cmd == 'scene3':
      scene3()
    if input_cmd == 'scene4':
      scene4()
    if input_cmd == 'scene5':
      scene5()
    if input_cmd == 'scene6':
      scene6()

def scene1():
    pyautogui.hotkey('ctrl', 'alt', 'shift', '1', interval=0.25)
    stoptimer()
    global timer
    timer = count_down('Scene: Cichlid Tank (', 40)
    timer.start()

def scene2():
    pyautogui.hotkey('ctrl', 'alt', 'shift', '2', interval=0.25)
    stoptimer()
    global timer
    timer = count_down('Scene: Cichlid Tank Fullscreen (', 20)
    timer.start()

def scene3():
    pyautogui.hotkey('ctrl', 'alt', 'shift', '3', interval=0.25)
    stoptimer()
    global timer
    timer = count_down('Scene: Salt Tank (', 40)
    timer.start()

def scene4(): 
    pyautogui.hotkey('ctrl', 'alt', 'shift', '5', interval=0.25)
    stoptimer()
    global timer
    timer = count_down('Scene: Salt Tank Fullscreen (', 20)
    timer.start()

def scene5():
    pyautogui.hotkey('ctrl', 'alt', 'shift', '4', interval=0.25)
    stoptimer()
    global timer
    timer = count_down('Scene: Dual View (')
    timer.start()

def scene6():
    pyautogui.hotkey('ctrl', 'alt', 'shift', '6', interval=0.25)
    stoptimer()
    global timer
    timer = count_down('Scene: Triple View (')
    timer.start()

def scenerotation(q):
  while True:
    scene1()
    timeralive()
    scene2()
    timeralive()
    scene3()
    timeralive()
    scene4()
    timeralive()
    scene5()
    timeralive()
#    scene6()
#    timeralive()


apexcube = {
  'url': 'http://xapexcube.x/cgi-bin/status.xml',
  'file': '/home/xero/misc/documents/apexcube.txt',
  'skip': ['Email2Alm_I9', 'Tmpx4'],
  'startswith': ['Unused', 'Snd', 'VarSpd', 'Link'],
  'endswith': ['Bright', 'Dim']
}

apex = {
  'url': 'http://xapex.x/cgi-bin/status.xml',
  'file': '/home/xero/misc/documents/apex',
  'skip': ['Salt', 'Email2Alm_I9'],
  'startswith': ['Unused', 'Snd', 'VarSpd', 'Link'],
  'endswith': []
}

q=queue.Queue(maxsize=1)

cpoller = threading.Thread(name='apexcube', target=apexpoller, args=(apexcube,))
apoller = threading.Thread(name='apex', target=apexpoller, args=(apex,))
spoller = threading.Thread(name='scene', target=scenerotation, args=(q,))

cpoller.start()
time.sleep(0.1)
apoller.start()

global timer
timer = []
spoller.start()
cmdinput()
