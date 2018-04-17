#!/usr/bin/env python

import rospy
import geometry_msgs
from gazebo_msgs.msg import ModelStates

def logModelStates(data):
    rospy.loginfo(data)

def position():
    rospy.init_node('position')
    rospy.Subscriber('gazebo/model_states', ModelStates, logModelStates)

    rospy.spin()

if __name__ == '__main__':
    position()
