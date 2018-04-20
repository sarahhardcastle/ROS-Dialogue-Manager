#!/usr/bin/env python

import rospy
import word_dict
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import String
from nltk.stem.snowball import SnowballStemmer

current_vel = 0
name = "turtlebot3_burger"
location = ""

def preprocessing(speech_data):
    global stemmer
    speech = []
    speech_list = speech_data.data.split()
    for word in speech_list:
        speech.append(stemmer.stem(word))
    print speech
    process_word(speech)

def process_word(word_list):
    word = word_list[0]
    if (word in word_dict.MOVE):
        process_movement(word, word_list[1:])
    elif(word_list[1:]):
        process_word(word_list[1:])    

def process_movement(move_word, word_list):
    print("Movement instruction detected")
    if(move_word == "stop"):
        print "Stopping"
        set_velocity(0,0)
    elif(word_list):
        word = word_list[0]
        print
        if(word in word_dict.DIRECTION):
            if (word == "forward"):
                print("Moving forwards")
                set_velocity(0.05,0)
            elif (word == "backward"):
                print("Moving backwards")
                set_velocity(-0.05,0)


def get_location(model_states):
    global location
    location_index = model_states.name.index(name)
    location = model_states.pose[location_index].position
    

def set_velocity(linear, angular):
    global vel_pub, current_vel
    print("Setting velocities: " + str(linear) + ", " + str(angular))
    new_velocity = Twist()
    new_velocity.linear.x = linear
    new_velocity.angular.z = angular
    current_vel = new_velocity
    vel_pub.publish(new_velocity)



def dialogue_manager():
    global vel_pub, stemmer

    rospy.init_node('dialogue_manager')
    stemmer = SnowballStemmer("english")

    rospy.Subscriber("speech", String, preprocessing)
    rospy.Subscriber('gazebo/model_states', ModelStates, get_location, queue_size=1)
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)

    rospy.init_node('dialogue_manager')

    stemmer = SnowballStemmer("english")

#    tts_pub = rospy.Publisher('tts', String, queue_size=3)
    rospy.init_node('dialogue_manager')

    rospy.spin()

if __name__ == '__main__':
    dialogue_manager()
