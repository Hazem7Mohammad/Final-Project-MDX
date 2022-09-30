#!/usr/bin/env python

from __future__ import print_function

import socket

from time import sleep

import sys
import rospy
from beginner_tutorials.srv import *

def add_two_ints_client(x, y):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts2) # recieve
        resp1 = add_two_ints(x, y)
        center=(resp1.sum1 , resp1.sum2)

# un comment for arm 
        # # Create a client socket
        # clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # # Connect to the server
        # clientSocket.connect(("192.168.150.2",2001))
        # # Send data to server


        print ("centre coordinates" +str(center))
        s= str(center)
        s1 = s.replace(",", "")
        print(s1)
        data = s1 +"\r\n"
        # data = " -660 314 \r\n"

# un comment for arm 
        # clientSocket.send(data.encode())
        # sleep(1)


        return center
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


if __name__ == "__main__":
    x = 0
    y = 0
    print("Requesting %s+%s"%(x, y))
    print(add_two_ints_client(x, y))






 

