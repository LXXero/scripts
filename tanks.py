#!/usr/bin/python
import threading
import requests
import xmltodict
import time
import pyautogui
import sys
from live import *

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

def privcmd(input_cmd):
  if input_cmd == 'stayscene1':
    scene1(3600, lock=True)
  if input_cmd == 'stayscene2':
    scene2(3600, lock=True)
  if input_cmd == 'stayscene3':
    scene3(3600, lock=True)
  if input_cmd == 'stayscene4':
    scene4(3600, lock=True)
  if input_cmd == 'stayscene5':
    scene5(3600, lock=True)
  if input_cmd == 'stayscene6':
    scene6(3600, lock=True)

def cmd(input_cmd):
  print ("Command Received " + input_cmd)
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
  if input_cmd == 'stayscene1':
    scene1(300)
  if input_cmd == 'stayscene2':
    scene2(300)
  if input_cmd == 'stayscene3':
    scene3(300)
  if input_cmd == 'stayscene4':
    scene4(300)
  if input_cmd == 'stayscene5':
    scene5(300)
  if input_cmd == 'stayscene6':
    scene6(300)

def cmdinput():
  while True:
    #print("timer is %s" % timer)
    input_cmd = input("Enter Command: ")
    cmd(input_cmd)

def scene(key, name, time, lock):
    pyautogui.hotkey('winleft', 'alt', 'shift', str(key), interval=0.1)
    stoptimer()
    global timer
    if lock:
      name = name + ' Locked'
    timer = count_down('Scene: '+name+' (', time)
    timer.start()
    if lock:
      time.sleep(time)

def scene1(time=40, lock=False):
    scene(1, 'Cichlid Tank', time, lock)

def scene2(time=20, lock=False):
    scene(2, 'Cichlid Tank Fullscreen', time, lock)

def scene3(time=40, lock=False):
    scene(3, 'Salt Tank', time, lock)

def scene4(time=20, lock=False): 
    scene(4, 'Salt Tank Fullscreen', time, lock)

def scene5(time=120, lock=False):
    scene(5, 'Dual View', time, lock)

def scene6(time=120, lock=False):
    scene(6, 'Triple View', time, lock)

def scenerotation():
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

def process_messages(youtube,liveChatId):
  #print("Messages for id '%s':" % liveChatId)

  list_chat_messages = youtube.liveChatMessages().list(
    liveChatId=liveChatId,
    part="id,snippet"
  )

  while list_chat_messages:
    list_messages_response = list_chat_messages.execute()

    cmdmessages = []
    #chatmessages = []
    for message in list_messages_response.get("items", []):
      if message["snippet"]["displayMessage"].startswith(tuple(['#', '!'])):
        cmdmessages.append({'author': message["snippet"]["authorChannelId"], 'message': message["snippet"]["displayMessage"]})
      #else:
      #  chatmessages.append({'author': message["snippet"]["authorChannelId"], 'message': message["snippet"]["displayMessage"]})

    try: 
      author = list_channel_titles(youtube, cmdmessages[-1]['author'])
      text = cmdmessages[-1]['message']

      if text.startswith('#'):
        cmd(text[1:])
      if author == 'LXXero' and text.startswith('!'):
        privcmd(text[1:])
    except:
      pass

    time.sleep(5)

    list_chat_messages = youtube.liveChatMessages().list_next(
      list_chat_messages, list_messages_response)



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

cpoller = threading.Thread(name='apexcube', target=apexpoller, args=(apexcube,))
apoller = threading.Thread(name='apex', target=apexpoller, args=(apex,))
spoller = threading.Thread(name='scene', target=scenerotation)
ipoller = threading.Thread(name='cmdinput', target=cmdinput)

cpoller.start()
time.sleep(0.1)
apoller.start()

global timer
timer = []
spoller.start()
ipoller.start()

if __name__ == "__main__":
  argparser.add_argument("--broadcast-status", help="Broadcast status",
    choices=VALID_BROADCAST_STATUSES, default=VALID_BROADCAST_STATUSES[1])
  args = argparser.parse_args()

  youtube = get_authenticated_service(args)
  try:
    liveChatId = list_broadcasts(youtube, args.broadcast_status)
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

#  print(liveChatId)

  while True:
    try:
      process_messages(youtube,liveChatId)
    except HttpError as e:
      print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
      time.sleep(5)

