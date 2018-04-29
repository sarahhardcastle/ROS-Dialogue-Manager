#!/usr/bin/env python

import rospy
import time
import word_dict
import language_processing as lp

from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import String

from sound_play.libsoundplay import SoundClient

current_vel = 0
name = "turtlebot3_burger"
location = ""
goal_location = (0,0)

def preprocessing(speech_data):
    global location
    sentences = []
    current_location = location
    speech_list = speech_data.data.lower().split('then')
    for sentence in speech_list:
        sentence = lp.process_sentence(sentence)

        if sentence[0][0] in ['Action', 'Direction']:
            action(sentence)
        elif sentence[0][0] = 'Question':
            sound_client.say("Sorry I don't understand your question")
        else:
            sound_client.say("Sorry I don't understand")
        

def action(sentence):
    if sentence[1][0] == 'stop':
        set_velocity(0,0)
    else:
        move_type = ''
        direction = 0
        move_time = 5
        speed = 0.1
        for i in range(0,len(sentence[1])):
            if sentence[1][i] in word_dict.MOVE:
                move_type = 'Linear'
            elif sentence[1][i] == 'turn':
                move_type = 'Angular'
            elif sentence[0][i] == 'Direction':
                if sentence[1][i].startswith('forw'):
                    print "direction: 1"
                    direction = 1
                elif sentence[1][i].startswith('back'):
                    print "direction: -1"
                    direction = -1
                elif sentence[1][i] in ['right', 'clockwise']:
                    move_type = 'Angular'
                    direction = 1
                elif sentence[1][i] in ['left', 'anticlockwise']:
                    move_type = 'Angular'
                    direction = -1    
            if sentence[0][i] == 'Number':
                move_time = sentence[1][i]
                print ("time: " + str(move_time))
            if sentence[0][i] == 'Adverb':
                print "speed detected"
                if sentence[1][i] in word_dict.FAST:
                    speed *= 2
                elif sentence[1][i] in word_dict.SLOW:
                    speed *= 0.5
        print (move_type, direction)

        if (move_type == 'Linear'):
            set_velocity(direction * speed, 0)
            time.sleep(move_time/(10*speed))
            set_velocity(0,0)
        elif (move_type == 'Angular'):
            set_velocity(0, direction * speed)
            time.sleep(move_time)
            set_velocity(0,0)
        else:
            sound_client.say("Sorry I only understand commands for movement")

    pass



def get_location(model_states):
    global location
    try:
        location_index = model_states.name.index(name)
        location = model_states.pose[location_index].position
    except ValueError:
        pass
    

def set_velocity(linear, angular):
    global vel_pub, current_vel
    print("Setting velocities: " + str(linear) + ", " + str(angular))
    new_velocity = Twist()
    new_velocity.linear.x = linear
    new_velocity.angular.z = angular
    current_vel = new_velocity
    vel_pub.publish(new_velocity)



def dialogue_manager():
    global vel_pub, sound_client

    rospy.init_node('dialogue_manager')

    rospy.Subscriber("speech", String, preprocessing)
    rospy.Subscriber('gazebo/model_states', ModelStates, get_location, queue_size=1)
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
    sound_client = SoundClient()

    rospy.init_node('dialogue_manager')

    rospy.init_node('dialogue_manager')

    rospy.spin()

if __name__ == '__main__':
    dialogue_manager()
