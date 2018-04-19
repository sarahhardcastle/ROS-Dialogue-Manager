#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import String


name = "turtlebot3_burger"
location = ""

def process_speech(speech_data):

    print(speech_data)

def set_location(model_states):
    location_index = model_states.name.index(name)
    location = model_states.pose[location_index].position
    print location


def dialogue_manager():
    rospy.Subscriber("speech", String, process_speech)
    rospy.Subscriber('gazebo/model_states', ModelStates, set_location, queue_size=1)
    movement_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)

#    tts_pub = rospy.Publisher('tts', String, queue_size=3)
    rospy.init_node('dialogue_manager')

    rospy.spin()

if __name__ == '__main__':
    dialogue_manager()
