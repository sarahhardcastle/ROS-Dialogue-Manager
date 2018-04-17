#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Point
from gazebo_msgs.msg import ModelStates

location = ""

#def process_speech(data):
#    pass

def get_location(name):
    print("Getting Location:")
    global location, object_name
    object_name = name
    model_state = rospy.Subscriber('gazebo/model_states', ModelStates, check_location, queue_size=10)
    
    print(location)
    return location

def check_location(model_states):
    global location, object_name
    rospy.loginfo(model_states)
    location_index = model_states.name.index(object_name)
    print(location_index)

    location = model_states.pose[location_index].position
    rospy.loginfo(location)


def dialogue_manager():
#    rospy.Subscriber("speech", String, process_speech)
#    movement_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
#    tts_pub = rospy.Publisher('tts', String, queue_size=3)
    rospy.init_node('dialogue_manager')

    get_location("turtlebot3_burger")

    rospy.spin()

if __name__ == '__main__':
    dialogue_manager()
