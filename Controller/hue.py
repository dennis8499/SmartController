
#!/usr/bin/python
import requests
import json
import hue_config
#url = "http://192.168.31.146/api/7UPoC4hXzygqWtYdzBQ2KhHc3j8xJ7SsHTIJAZ0V/lights/2/state"
#IP = '10.0.1.35'
#username = 'D8vw1zJyzne37L-VDnfPlJwZlNw5uhkHY8epELwQ'
light1 = '/lights/1'
light2 = '/lights/2'
light3 = '/lights/3'
state = '/state'
http = "http://"
groups = "/groups/"
groupsName = "aaa"
action = "/action"
#data_on ={"on":True,"bri":bri,"sat":255,"hue":0}
StateColor = 0
StateBri = 0
url = ''
IP = hue_config.getIp()
username = hue_config.getUserName()
def lightOn(pos):
  global url
  if (pos == '1'):
      url = http + IP + '/api/' + username + light1 + state
  elif (pos == '2'):
      url = http + IP + '/api/' + username + light2 + state
  elif (pos == '3'):
      url = http + IP + '/api/' + username + light3 + state
  elif (pos == '4'):
      url = http + IP + '/api/' + username + groups + groupsName + action
  try:

      data_on ={"on":True}
      r = requests.put(url, json.dumps(data_on), timeout=5)
  except:
      print("Hue not in the internet")
def lightOff(pos):
  global url
  if (pos == '1'):
      url = http + IP + '/api/' + username + light1 + state
  elif (pos == '2'):
      url = http + IP + '/api/' + username + light2 + state
  elif (pos == '3'):
      url = http + IP + '/api/' + username + light3 + state
  elif (pos == '4'):
      url = http + IP + '/api/' + username + groups + groupsName + action
  try:
      data_off = {"on":False}
      r = requests.put(url, json.dumps(data_off), timeout=5)
  except:
      print("Hue not in the internet")

def brightness(pos, bri):
  global url
  if (pos == '1'):
      url = http + IP + '/api/' + username + light1 + state
  elif (pos == '2'):
      url = http + IP + '/api/' + username + light2 + state
  elif (pos == '3'):
      url = http + IP + '/api/' + username + light3 + state
  elif (pos == '4'):
      url = http + IP + '/api/' + username + groups + groupsName + action
  try:
      data_Brightness = {"bri":int(bri)}
      r = requests.put(url, json.dumps(data_Brightness), timeout=5)
  except:
      print("Hue not in the internet")

def awsOn(pos, color, bri):
  global StateColor, StateBri, url
  if (pos == '1'):
      url = http + IP + '/api/' + username + light1 + state
  elif (pos == '2'):
      url = http + IP + '/api/' + username + light2 + state
  elif (pos == '3'):
      url = http + IP + '/api/' + username + light3 + state
  elif (pos == '4'):
      url = http + IP + '/api/' + username + groups + groupsName + action

  if (color == '1'):
      StateColor = 12750 #yellow
  elif(color == '2'):
      StateColor = 25500 #green
  elif(color == '3'):
      StateColor = 46920 #blue
  elif(color == '4'):
      StateColor = 56100 #purple

  if (bri == '1'):
      StateBri = 0
  elif (bri == '2'):
      StateBri = 100
  elif (bri == '3'):
      StateBri = 255
  try:
      data_awsOn = {"on":True, "bri":int(StateBri), "hue":int(StateColor)}
      r = requests.put(url, json.dumps(data_awsOn), timeout=5)
  except:
      print("Hue not in the internet")

def awsOff(pos):
  global url
  if (pos == '1'):
      url = http + IP + '/api/' + username + light1 + state
  elif (pos == '2'):
      url = http + IP + '/api/' + username + light2 + state
  elif (pos =='3'):
      url = http + IP + '/api/' + username + light3 + state
  elif (pos == '4'):
      url = http + IP + '/api/' + username + groups + groupsName + action
  try:
      data_awsOff = {"on":False}
      r = requests.put(url, json.dumps(data_awsOff), timeout=5)
  except:
      print("Hue not in the internet")
