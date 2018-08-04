from imp import load_source
WalabotAPI = load_source('WalabotAPI',
'/usr/share/walabot/python/WalabotAPI.py')

WalabotAPI.Init() # Init the Wallabot.

# Get the status of the device.
appStatus, calibrationProcess = WalabotAPI.GetStatus()
#Connect the Wallbot
try:# try to connect to the walabot.
	WalabotAPI.ConnectAny()
except WalabotError as err:# Evaluate if the walabot is not connected.
	if err.message == WalabotAPI.WALABOT_INSTRUMENT_NOT_FOUND:
   print('Please connect your Walabot')