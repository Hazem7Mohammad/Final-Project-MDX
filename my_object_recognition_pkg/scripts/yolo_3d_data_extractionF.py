#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from gb_visual_detection_3d_msgs.msg import BoundingBoxes3d

# chatter added 
from geometry_msgs.msg import Pose2D
import sys

class Yolo3DFilter:

   def __init__(self, object_name_to_search, accepted_probability=0.2):              # test 

      self._rate = rospy.Rate(1)                                                     # test 

      self._object_name_to_search = object_name_to_search
      self._accepted_probability = accepted_probability
      self.objects_dict = {}
      self.yolo_3d_topic = "/darknet_ros_3d/bounding_boxes"
      self._check_yolo_3d_ready()
      rospy.Subscriber(self.yolo_3d_topic, BoundingBoxes3d, self.yolo_3d_clb)
     
      rospy.loginfo('Ready to detect with Yolo!')

   def _check_yolo_3d_ready(self):
      yolo_3d_data = None
      while yolo_3d_data is None and not rospy.is_shutdown():
         try:
               yolo_3d_data = rospy.wait_for_message(self.yolo_3d_topic, BoundingBoxes3d, timeout=1.0)         # test 
               rospy.logdebug("Current "+self.yolo_3d_topic+" READY=>" + str(yolo_3d_data))

         except:
               rospy.logerr("Current "+self.yolo_3d_topic+" not ready yet, retrying.")

   def update_object_name_to_search(self,new_name):
      self._object_name_to_search = new_name

   def calculate_center(self,box_data):

      x_center = (box_data.xmin + box_data.xmin) / 2.0
      y_center = (box_data.ymin + box_data.ymin) / 2.0
      z_center = (box_data.zmin + box_data.zmin) / 2.0

      Y = (y_center)*500
      Z = -300-(((z_center)*72)*10)       
      X = 300+(((x_center) * 104)*10)

      newX = int(Z)
      newY = int(X)
      center = (newX, newY)
      # print (center)

# chatter added 
      pub =rospy.Publisher('chatter', Pose2D, queue_size=1)           # test 
      position = Pose2D()
      position.x = newX
      position.y = newY 
      position.theta = int(Y)
      # rospy.loginfo(mat) 
      pub.publish(position)

      rospy.Timer(rospy.Duration(120), my_callback)

      return [newX, newY, int(Y)]

   def yolo_3d_clb(self, msg):

      # We clean the dict
      self.objects_dict = {}
      detect_object_index = 0

      detection_boxes_array = msg.bounding_boxes
      
      for box in detection_boxes_array:
         object_name = box.Class
         detection_probability = box.probability
         if object_name == self._object_name_to_search:
            if detection_probability >= self._accepted_probability:
               center_array = self.calculate_center(box)  
               unique_object_name = object_name+str(detect_object_index)             
               self.objects_dict[unique_object_name] = center_array
               
               detect_object_index += 1
            else:
               rospy.logdebug("Probability too low=="+str(detection_probability)+"<"+str(self._accepted_probability))
         else:
            rospy.logdebug("Object name doenst match="+str(object_name)+","+str(self._object_name_to_search))


   def get_objects_dict_detected(self):
      return self.objects_dict

   def run(self):


      while not rospy.is_shutdown():
         searched_for_objects_detected = self.get_objects_dict_detected()
         rospy.loginfo(str(searched_for_objects_detected))
         self._rate.sleep()

def my_callback(event):
   rospy.signal_shutdown("hi")

if __name__ == '__main__':
   rospy.init_node('search_for_object_node', log_level=rospy.INFO)

   # edited lines 
   object_name_to_search= sys.argv [1]
   for arg in sys.argv:
      print (arg)
   yolo_obj = Yolo3DFilter(object_name_to_search)

   try:
      yolo_obj.run()
   except KeyboardInterrupt:
      rospy.loginfo('Shutting down')
