#!/usr/bin/env python
# license removed for brevity
import rospy 
from std_msgs.msg import String

def talker():
    pub =rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) #10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str) 
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

# hello_str = rospy.get_param('~dude') 
# use this up when u want to put a param in argument in command 
# rosrun pde4420_session2 talker.py _dude:="Hello"
# 