import paho.mqtt.client as mqtt
import os, urlparse
from threading import Thread




class MQTTHelper (Thread):
	# Define event callbacks
	def on_connect(self,client, userdata, flags, rc):
		print("rc: " + str(rc))

	def on_message(self,client, obj, msg):
		#print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
		self.lastImage = str(msg.payload)

	def on_publish(self,client, obj, mid):
		print("mid: " + str(mid))


	def on_subscribe(self,client, obj, mid, granted_qos):
		print("Subscribed: " + str(mid) + " " + str(granted_qos))

	def on_log(self,client, obj, level, string):
		print(string)	


	def sendMessage (self,topic,message):
		self.mqttc.publish(topic, message)

	def run(self):
		# Continue the network loop, exit when an error occurs
		rc = 0
		while rc == 0:
			rc = self.mqttc.loop()
			#print("rc: " + str(rc))


	def __init__(self):
		Thread.__init__(self)
		
		self.lastImage = None
		self.mqttc = mqtt.Client()
		# Assign event callbacks
		self.mqttc.on_message = self.on_message
		self.mqttc.on_connect = self.on_connect
		self.mqttc.on_publish = self.on_publish
		self.mqttc.on_subscribe = self.on_subscribe
		# Uncomment to enable debug messages
		#mqttc.on_log = on_log
		# Parse CLOUDMQTT_URL (or fallback to localhost)
		self.url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://spectacular-hairdresser.cloudmqtt.com:1883')
		self.url = urlparse.urlparse(self.url_str)
		self.topic =  'gotouch'
		# Connect
		self.mqttc.username_pw_set('hkadwsqx', 'BCTi-JnC_3Hg')
		self.mqttc.connect(self.url.hostname, self.url.port)

		# Start subscribe, with QoS level 0
		self.mqttc.subscribe(self.topic, 0)

		# Publish a message
		#self.mqttc.publish(self.topic, "gotouch")

	def getLastImg(self):
		return self.lastImage

			
		
#mqtt = MQTTHelper()
#mqtt.start()
#mqtt.sendMessage ("test","message gt")



