#!/usr/bin/env python
import os
import rospy 
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge

from duckietown import DTROS 
from std_msgs.msg import String
from duckietown_msgs.msg import WheelsCmdStamped, BoolStamped
from duckietown_msgs.msg import LEDPattern
from duckietown_msgs.srv import SetCustomLEDPattern,ChangePattern

class MyNode(DTROS):
	def __init__(self, node_name):
		# initialize the DTROS parent class
		super(MyNode, self).__init__(node_name=node_name)
		# construct publisher
		self.pub = rospy.Publisher('/duckiebot7/wheels_driver_node/wheels_cmd', WheelsCmdStamped ,queue_size=1)
		self.sub = self.subscriber('/duckibot7/camera_node/image/compressed',CompressedImage,self.onImageReceived)

	def onImageReceived(self,msg):

		np_arr = np.fromstring(msg.data,np.uint8)
		image_np = cv2.imdecode(np_arr,cv2.IMREAD_COLOR)

		bridge = CvBridge()
		image_message = bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")

	def run(self):
		# publish message every 1 second
		rate = rospy.Rate(1) # 1Hz    

		rospy.sleep(5)

		rospy.wait_for_service('/duckiebot7/led_emitter_node/set_custom_pattern')

		try:
			service = rospy.ServiceProxy('/duckiebot7/led_emitter_node/set_custom_pattern',SetCustomLEDPattern)
			msg = LEDPattern()
			msg.color_list = ['white','switchedoff','white','switchedoff','white']
			msg.color_mask = [1,1,1,1,1]
			msg.frequency = 1.0
			msg.frequency_mask = [0,0,0,0,0]
			response = service(msg)
			rospy.loginfo(response)

		except rospy.ServiceException, e:

			print"Service call failed: %s"%e


		while not rospy.is_shutdown():

			msg = WheelsCmdStamped()
			msg.header.stamp = rospy.get_rostime()

			rospy.sleep(2)

			msg.vel_left = 0.4
			msg.vel_right = 0.4
			self.pub.publish(msg)  

			rospy.sleep(2)

			rospy.wait_for_service('/duckiebot7/led_emitter_node/set_custom_pattern')

			try:
				service = rospy.ServiceProxy('/duckiebot7/led_emitter_node/set_custom_pattern',SetCustomLEDPattern)
				msg = LEDPattern()
				msg.color_list = ['yellow','switchedoff','white','switchedoff','white']
				msg.color_mask = [1,1,1,1,1]
				msg.frequency = 1.0
				msg.frequency_mask = [1,0,0,0,0]
				response = service(msg)
				rospy.loginfo(response)

			except rospy.ServiceException, e:

				print"Service call failed: %s"%e
			
			msg = WheelsCmdStamped()
			msg.header.stamp = rospy.get_rostime()
			msg.vel_left = -0.4
			msg.vel_right = 0.4
			self.pub.publish(msg)  

			rospy.sleep(1)
			rospy.wait_for_service('/duckiebot7/led_emitter_node/set_custom_pattern')

			try:
				service = rospy.ServiceProxy('/duckiebot7/led_emitter_node/set_custom_pattern',SetCustomLEDPattern)
				msg = LEDPattern()
				msg.color_list = ['white','switchedoff','white','switchedoff','white']
				msg.color_mask = [1,1,1,1,1]
				msg.frequency = 1.0
				msg.frequency_mask = [0,0,0,0,0]
				response = service(msg)
				rospy.loginfo(response)

			except rospy.ServiceException, e:

				print"Service call failed: %s"%e
			
			msg = WheelsCmdStamped()
			msg.header.stamp = rospy.get_rostime()
			msg.vel_left = 0.4
			msg.vel_right = 0.4
			self.pub.publish(msg)  

			rospy.sleep(2)

			rospy.wait_for_service('/duckiebot7/led_emitter_node/set_custom_pattern')

			try:
				service = rospy.ServiceProxy('/duckiebot7/led_emitter_node/set_custom_pattern',SetCustomLEDPattern)
				msg = LEDPattern()
				msg.color_list = ['white','red','white','red','white']
				msg.color_mask = [1,1,1,1,1]
				msg.frequency = 1.0
				msg.frequency_mask = [0,0,0,0,0]
				response = service(msg)
				rospy.loginfo(response)

			except rospy.ServiceException, e:

				print"Service call failed: %s"%e


			self.stop()     

			rate.sleep()
			break

	def onShutdown(self):

		msg = WheelsCmdStamped()
		msg.header.stamp = rospy.get_rostime()
		msg.vel_left = 0
		msg.vel_right = 0

		self.pub.publish(msg) 

	def stop(self):
		msg = WheelsCmdStamped()
		msg.header.stamp = rospy.get_rostime()
		msg.vel_left = 0
		msg.vel_right = 0
		self.pub.publish(msg)      
			
if __name__ == '__main__':    
	# create the node    
	node = MyNode(node_name='my_node')    
	# run node    
	node.run()
	# keep spinning    
	#rospy.spin()



