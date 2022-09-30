#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import rospy
from gb_visual_detection_3d_msgs.msg import BoundingBoxes3d
from beginner_tutorials.srv import *

import socket

# chatter added 
from geometry_msgs.msg import Pose2D

# variables 
locationX = []
locationY = []
locationZ = []

# most commone number
def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num


#subscriber
def radar_callback(input_radar):
    locationX.append(input_radar.x)
    locationY.append(input_radar.y)
    locationZ.append(input_radar.theta)   

    print (len(locationX),len(locationY),len(locationZ))
    
    if len(locationX) > 25:                                       
        
        # sub.unregister()
        n = 5                                                     
        del locationX[:n]
        del locationY[:n]
        del locationZ[:n]

    global Y
    global X
    global Z
    
    Y = most_frequent(locationY)
    Z = most_frequent(locationZ)       
    X = most_frequent(locationX) 

    # print (X,Y,Z)
    print("{:.2f}".format(X),"{:.2f}".format(Y),"{:.2f}".format(Z))
 
    
def handle_add_two_ints(req):
    return AddTwoInts2Response(req.a+X , req.b+Y)

def add_two_ints_server():
    s = rospy.Service('add_two_ints', AddTwoInts2, handle_add_two_ints) # send
    print("Ready to add two ints.")
    rospy.spin()


if __name__ == '__main__':    
    rospy.init_node('listener')
    print ("HELLO")
    rospy.Subscriber("/chatter", Pose2D, radar_callback)
    add_two_ints_server() 
    rospy.spin()


