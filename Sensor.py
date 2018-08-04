from imp import load_source
from os import system
WalabotAPI = load_source('WalabotAPI',
'/usr/share/walabot/python/WalabotAPI.py')



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
	appStatus, calibrationProcess = WalabotAPI.GetStatus()
	while ( appStatus == WalabotAPI.STATUS_CALIBRATING ):
		system("clear")
		print("Calibrating Process",calibrationProcess)
		appStatus, calibrationProcess = WalabotAPI.GetStatus()

	appStatus, calibrationProcess = WalabotAPI.GetStatus()	
	walabotStatus()

def configureWalabot():
	# Short-range, penetrative scanning inside dielectric materials such as walls.
	WalabotAPI.SetProfile(WalabotAPI.PROF_SHORT_RANGE_IMAGING)# short range 
	#No need to remove weak signal. We are not focused on moving targets.
	WalabotAPI.SetDynamicImageFilter(WalabotAPI.FILTER_TYPE_NONE)
	print("Walabot Configured")








WalabotAPI.Init() # Init the Wallabot.
#Connect the Wallbot
connectWalabot()
#calibrate the walabot
calibrateWalabot()
# configure the walabot
configureWalabot()
