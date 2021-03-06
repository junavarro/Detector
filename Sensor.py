from imp import load_source
from os import system
import matplotlib.pyplot as plt 
import numpy as np
WalabotAPI = load_source('WalabotAPI',
'/usr/share/walabot/python/WalabotAPI.py')
from threading import Thread
import MQTTClient
from PIL import Image





def walabotStatus():
	appStatus, calibrationProcess = WalabotAPI.GetStatus()	
	switcher = {
	WalabotAPI.STATUS_DISCONNECTED: "DISCONNECTED",
	WalabotAPI.STATUS_CONNECTED: "CONNECTED",
	WalabotAPI.STATUS_IDLE: "IDLE",
	WalabotAPI.STATUS_SCANNING: "SCANNING",
	WalabotAPI.STATUS_CALIBRATING: "CALIBRATING"
	}
	print switcher.get(appStatus, "Invalid status")


def connectWalabot():
	try: 
		WalabotAPI.ConnectAny()
		WalabotAPI.SetSettingsFolder()
		print('Walabot connected')
	except WalabotError as err:# Evaluate if the walabot is not connected.
		if err.message == WalabotAPI.WALABOT_INSTRUMENT_NOT_FOUND:
			print('Please connect your Walabot')

def calibrateWalabot():
	print("Init Calibration")
	WalabotAPI.StartCalibration()
	appStatus, calibrationProcess = WalabotAPI.GetStatus()

	#while ( appStatus == WalabotAPI.STATUS_CALIBRATING ):
		#system("clear")
		#print("Calibrating Process",calibrationProcess)
		#appStatus, calibrationProcess = WalabotAPI.GetStatus()

	appStatus, calibrationProcess = WalabotAPI.GetStatus()	
	walabotStatus()

def configureWalabot():
	#Define the arena
	
	# Short-range, penetrative scanning inside dielectric materials such as walls.
	WalabotAPI.SetProfile(WalabotAPI.PROF_SHORT_RANGE_IMAGING)# short range 
	# Select scan arena
	#             R             Phi          Theta
	ARENA = [(1, 50, 1), (-60, 60, 2), (-60, 60, 2)]
	# Set scan arena
	WalabotAPI.SetArenaR(*ARENA[0])
	WalabotAPI.SetArenaPhi(*ARENA[1])
	WalabotAPI.SetArenaTheta(*ARENA[2])
	WalabotAPI.SetThreshold(1)
	#No need to remove weak signal. We are not focused on moving targets.
	WalabotAPI.SetDynamicImageFilter(WalabotAPI.FILTER_TYPE_NONE)
	print("Walabot Configured")

def startWalabot():
	WalabotAPI.Start()

def getData():
	rasterImage, test1, test2, sliceDepth, power = WalabotAPI.GetRawImageSlice()
	mqtt = MQTTClient.MQTTHelper()
	mqtt.start()
	while True:
		WalabotAPI.Trigger()    
		targets = WalabotAPI.GetImagingTargets()
		print(WalabotAPI.GetRawImageSlice())
		rasterImage, test1, test2, sliceDepth, power = WalabotAPI.GetRawImageSlice()
		system("clear")
		#print(rasterImage)
		print("Test 1: ", test1)
		print("Test 2: ", test2)
		print("Rows:  ", len(rasterImage))
		print("Cols:  ", len(rasterImage[0]))
		print("Slide Depth: ",sliceDepth)
		print("Power: ", power)
		mqtt.sendMessage ("gotouch",str(rasterImage))
		#img = Image.fromarray(np.array(rasterImage), 'RGB')
		#print(np.array(rasterImage))
		#img.save('my.png')
		image = plt.imshow(np.array(rasterImage), interpolation='nearest')
		plt.pause(0.05)
	plt.show()
		
		#walabotplot.updateGraph(rasterImage)

		

		






WalabotAPI.Init() # Init the Wallabot.
#Connect the Wallbot
connectWalabot()
# configure the walabot
configureWalabot()
#start
startWalabot()
#calibrate the walabot
calibrateWalabot()

#get the image
getData()