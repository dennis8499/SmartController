#!/usr/bin/python
#********SnowBoy********
import snowboydecoder
import os
import re
import sys
import signal
import subprocess
#***********************
#*********System********
import RPi.GPIO as GPIO
import threading
import time
#***********************
#********AWSIOT*********
import uuid
import json
import requests
import argparse
import logging
import urllib2
from AWSIoTPythonSDK.core.greengrass.discovery.providers import DiscoveryInfoProvider
from AWSIoTPythonSDK.core.protocol.connection.cores import ProgressiveBackOffCore
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryInvalidRequestException
from subprocess import check_output
#***********************
#***********************
import config
#***********************
#-----------------------
#*********AWSIOT********
host = 'ar601rxs1vs54.iot.us-east-1.amazonaws.com'
rootCAPath = 'cert/root-ca-cert.pem'
certificatePath = 'cert/d3af6dd0c9.cert.pem'
privateKeyPath = 'cert/d3af6dd0c9.private.key'
thingName = 'GreenGrass_Smart_Controler'
clientId2 = 'GreenGrass_Smart_Controler'
#clientId2 = 'Zero W2'
topic = 'GreenGrass/Assistant/Receiver'
MAX_DISCOVERY_RETRIES = 10
GROUP_CA_PATH = "./groupCA/"
retryCount = MAX_DISCOVERY_RETRIES
discovered = False
groupCA = None
coreInfo = None
GreenGrassAWSIoTMQTTClient = None
myDeviceShadow = None
#***********************
#**********pin**********
SW = 27
#***********************
#*********State***********
wifiState = True
#*************************
#********rotary*********
wifi_detect = 0
#*************************
#*************************
detector = None
#*************************
#*******SnowBoy***********
interrupted = False
model = "resources/alexa.pmdl"
hotword = 0
#*************************
def wifiConnect(): #偵測有無網路
	try:
		subprocess.check_output(["ping", "-c", "3", "-W", "3", "8.8.8.8"])
		return True
	except:
		return False
def wifiDetect(): #使用執行緒來偵測網路，如果偵測超過3次就發出wifi disconnected，如果途中正常則計數器歸零
	global wifi_detect, wifiState
	while True:
		Status = wifiConnect()
		#print "WIFI: " + str(wifi_detect)
		if (Status == False):
			wifiState = False
			wifi_detect = wifi_detect + 1
			if (wifi_detect == 3):
				subprocess.Popen(['mpg321', 'sound/wifi_disconnected.mp3']).wait()
		elif(Status == True):
			if (wifiState == False):
				wifiState = True
				subprocess.Popen(['mpg321', 'sound/wifi_connected.mp3']).wait()
			wifi_detect = wifi_detect - 1;
			if (wifi_detect < 0): wifi_detect = 0
		time.sleep(10)
def setupReset(): #設定沒有網路時的按鍵
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def resetWifi(): #長壓rotary_encoder的按鈕五秒 重設網路
    setupReset()
    os.system('aplay /home/pi/RaspiWiFi/Reset\ Device/button_chime.wav')
    while True:
		if (GPIO.input(SW) == 0):
			startTime = time.time() * 1000
			while (GPIO.input(SW) == 0):
				continue
			endTime = time.time() * 1000
			duration = endTime - startTime
			print (duration)
			if (duration >= 5000) :
				os.system('aplay /home/pi/RaspiWiFi/Reset\ Device/button_chime.wav')
				os.system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
				os.system('rm -f /home/pi/RaspiWifi/tmp/*')
				os.system('sudo cp -r /home/pi/project/Reset\ Device/static_files/dhcpd.conf /etc/dhcp/')
				os.system('sudo cp -r /home/pi/project/Reset\ Device/static_files/hostapd.conf /etc/hostapd/')
				os.system('sudo cp -r /home/pi/project/Reset\ Device/static_files/interfaces.aphost /etc/network/interfaces')
				os.system('sudo cp -r /home/pi/project/Reset\ Device/static_files/isc-dhcp-server.aphost /etc/default/isc-dhcp-server')
				os.system('sudo cp -r /home/pi/project/Reset\ Device/static_files/rc.local.aphost /etc/rc.local')
				os.system('sudo cp -r /home/pi/project/app_start2.sh /home/pi/project/app_start.sh')
				os.system('sudo reboot')
def loggerSetting(): #顯示log
	logger = logging.getLogger("AWSIoTPythonSDK.core")
	logger.setLevel(logging.DEBUG)
	streamHandler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	streamHandler.setFormatter(formatter)
	logger.addHandler(streamHandler)
def GreenGrassCoreDiscovery(): #尋找網域內的greengrass core
	global groupCA, coreInfo
	# Progressive back off core
	backOffCore = ProgressiveBackOffCore()
	# Discover GGCs
	discoveryInfoProvider = DiscoveryInfoProvider()
	discoveryInfoProvider.configureEndpoint(host)
	discoveryInfoProvider.configureCredentials(rootCAPath, certificatePath, privateKeyPath)
	discoveryInfoProvider.configureTimeout(10)  # 10 sec
	retryCount = MAX_DISCOVERY_RETRIES
	discovered = False
	groupCA = None
	coreInfo = None
	while retryCount != 0:
		try:
			discoveryInfo = discoveryInfoProvider.discover(thingName)
			caList = discoveryInfo.getAllCas()
			coreList = discoveryInfo.getAllCores()
			# We only pick the first ca and core info
			groupId, ca = caList[0]
			coreInfo = coreList[0]
			print("Discovered GGC: %s from Group: %s" % (coreInfo.coreThingArn, groupId))
			print("Now we persist the connectivity/identity information...")
			groupCA = GROUP_CA_PATH + groupId + "_CA_" + str(uuid.uuid4()) + ".crt"

			if not os.path.exists(GROUP_CA_PATH):
				os.makedirs(GROUP_CA_PATH)
			groupCAFile = open(groupCA, "w")
			groupCAFile.write(ca)
			groupCAFile.close()
			discovered = True
			print("Now proceed to the connecting flow...")
			break
		except DiscoveryInvalidRequestException as e:
			print("Invalid discovery request detected!")
			print("Type: %s" % str(type(e)))
			print("Error message: %s" % e.message)
			print("Stopping...")
			break
		except BaseException as e:
			print("Error in discovery!")
			print("Type: %s" % str(type(e)))
			print("Error message: %s" % e.message)
			retryCount -= 1
			print("\n%d/%d retries left\n" % (retryCount, MAX_DISCOVERY_RETRIES))
			print("Backing off...\n")
			backOffCore.backOff()
	if not discovered:
		subprocess.Popen(['mpg321', 'sound/GreenGrass.mp3']).wait()
		print("Discovery failed after %d retries. Exiting...\n" % (MAX_DISCOVERY_RETRIES))
		sys.exit(-1)
def greengrass_iot_connect(): #連接Greengrass 的 aws iot mqtt
	global GreenGrassAWSIoTMQTTClient
	GreenGrassAWSIoTMQTTClient = AWSIoTMQTTClient(thingName)
	GreenGrassAWSIoTMQTTClient.configureCredentials(groupCA, privateKeyPath, certificatePath)
	GreenGrassAWSIoTMQTTClient.onMessage = customOnMessage
	connected = False
	for connectivityInfo in coreInfo.connectivityInfoList:
		currentHost = connectivityInfo.host
		currentPort = connectivityInfo.port
		print("Trying to connect to core at %s:%d" % (currentHost, currentPort))
		GreenGrassAWSIoTMQTTClient.configureEndpoint(currentHost, currentPort)
		try:
			GreenGrassAWSIoTMQTTClient.connect()
			connected = True
			break
		except BaseException as e:
			print("Error in connect!")
			print("Type: %s" % str(type(e)))
			print("Error message: %s" % e.message)
	if not connected:
		print("Cannot connect to core %s. Exiting..." % coreInfo.coreThingArn)
		subprocess.Popen(['mpg321', 'sound/AWSIOT.mp3'])
		sys.exit(-2)
def customOnMessage(message): #接受來自greengrass的lambda按鈕的訊息
	global myDeviceShadow
	print (message.payload)
    if(message.topic == "GreenGrass/Assistant/hue"):
		msg = json.loads(message.payload)
		if (msg['control'] == "hue"):
			url = msg['url']
			data_on = msg["data_on"]
			try:
				data_on = json.loads(data_on)
				r = requests.put(url, json.dumps(data_on), timeout=5)
			except:
				print("Hue not in the Internet or error")
	elif(message.topic == "GreenGrass/Assistant/Receiver"):
		if (message.payload == "on_hot_word"):
			on_hot_word()
		elif (message.payload == "resetWifi"):
			resetWifi()
def threadSetting(): #執行緒設定 分別為snowboy、wifiDetect
	global detector, model
	detector = snowboydecoder.HotwordDetector(model, sensitivity=0.4)
	wifiDetect_thread = threading.Thread(target = wifiDetect)
	wifiDetect_thread.start()
def shadow_connect(): #連接shadow
	global myShadowClient
	# read GGC Host Address from file
	myShadowClient = AWSIoTMQTTShadowClient(clientId2)
	myShadowClient.configureEndpoint(host, 8883)
	myShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
	myShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
	myShadowClient.configureConnectDisconnectTimeout(10)
	myShadowClient.configureMQTTOperationTimeout(5)

	myShadowClient.connect()
def shadow_setting(): #設定shadow
	global myDeviceShadow, myShadowClient
	myDeviceShadow = myShadowClient.createShadowHandlerWithName(thingName, True)
	IP = config.getIp()
	USERNAME = config.getUserName()
	print (IP + ":" + USERNAME)
	JSONPayload = '{"state":{"reported":{"controlstate":{"control": '+ '\"hue\"' + ', "IP": ' +'\"' +str(IP) +'\"' + ', "username": ' + '\"' +USERNAME + '\"'  + '}}}}'
	print (JSONPayload)
	myDeviceShadow.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)
def on_hot_word(): #關鍵字偵測
	global detector, hotword, interrupted
	print ("on_hot_word")
	detector.terminate()
	hotword = 1
	interrupted = True
def snowboyStart(): #Snowboy啟動
	global detector, hotword, interrupted, myDeviceShadow
	if (hotword == 1):
		Status = wifiConnect()
		if Status == True:
			subprocess.Popen(["node", "lex.js"]).wait()
		elif Status == False:
			subprocess.Popen(['mpg321', 'sound/access_lex.mp3']).wait()
		print("Restarting...")
		hotword = 0
	interrupted = False
	subprocess.Popen(['mpg321','resources/beep.mp3']).wait()
	detector.start(detected_callback = on_hot_word, interrupt_check = interrupt_callback, sleep_time = 0.03)
	subprocess.Popen(['mpg321','resources/beep.mp3']).wait()
	print ("detector stop")
def customShadowCallback_Update(payload, responseStatus, token): #當shadow更新時顯示訊息
	if responseStatus == "timeout":
		print("Update request " + token + " time out!")
	if responseStatus == "accepted":
		payloadDict = json.loads(payload)
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Update request with token: " + token + " accepted!")
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if responseStatus == "rejected":
		print("Update request " + token + " rejected!")
def signal_handler(signal, frame): #偵測到訊號
	global interrupted
	interrupted = True
def interrupt_callback(): #確認interrupted狀態
	global interrupted
	return interrupted

if __name__ == '__main__': #main 一開始先確認有無網路，有的話才開始啟動greengrass跟其他功能
	Status = wifiConnect()
	if (Status == True):
		subprocess.Popen(['mpg321', 'sound/wifi_connected.mp3']).wait()
		subprocess.Popen(['sh', 'greengrass_start.sh']).wait()
		time.sleep(5)
		loggerSetting()
		print ("LoggerSetting done")
		GreenGrassCoreDiscovery()
		print ("Discover GGCs done")
		greengrass_iot_connect()
		print ("GreenGrassIoTGreenGrass done")
		threadSetting()
		print("Program Start")
		shadow_connect()
		shadow_setting()
		print("shadow_setting done")
		subprocess.Popen(['mpg321','resources/system_already.mp3']).wait()
		while True:
			try:
				snowboyStart()
			except KeyboardInterrupt:
				GPIO.cleanup()
	elif (Status == False):
		subprocess.Popen(['mpg321', 'sound/wifi_disconnected.mp3']).wait()
		setupReset()
		resetWifi()
