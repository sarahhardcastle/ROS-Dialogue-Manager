#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist, Point

linear_vel = 0
angular_vel = 0    
angle = 0
coordinates = Point()
coordinates.x = 0; coordinates.y = 0; coordinates.z = 0;


def update_velocities(new_velocities):
    global angular_vel, linear_vel
    angular_vel = new_velocities.angular.z
    linear_vel = new_velocities.linear.x

def update_location(event):
    global angle, coordinates
    angle += angular_vel * 0.1
    if (angle > 2*math.pi):
        angle -= 2*math.pi
    elif (angle < 0):
        angle += 2*math.pi
    coordinates.x += linear_vel * 0.1 * math.cos(angle)
    coordinates.y += linear_vel * 0.1 * math.sin(angle)
    # angular velocity of 1 = 1 rad/second

def print_location(event):
    print("x: " + str(coordinates.x) + ", y: " + str(coordinates.y) + ", angle: " + str(angle))

def dead_reckoning(): 
    rospy.init_node('dead_reckoning')
    rospy.Subscriber('/cmd_vel', Twist, update_velocities)
    #listen in on messages about velocity sent to gazebo
    rospy.Timer(rospy.Duration(0.1), update_location, oneshot=False)
    #update location 10 times a second
    rospy.Timer(rospy.Duration(5), print_location, oneshot=False)
    rospy.spin()

if __name__ == "__main__":
    dead_reckoning()

