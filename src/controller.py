#!/usr/bin/env python3
from cmath import pi
import math
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

x_current = 0
y_current = 0
angle_current = 0

def pose_seperator(msg : Pose):
    global x_current
    x_current = msg.x
    global y_current
    y_current = msg.y
    global angle_current 
    angle_current = msg.theta

def quarter(x, y):
    if x<0 and y<0:
        return pi
    else:
        return 0

def main():
    rospy.init_node('controller')

    x_goal = rospy.get_param('/x_goal')
    y_goal = rospy.get_param('/y_goal')
    beta = rospy.get_param('/beta')
    theta = rospy.get_param('/theta')

    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/turtle1/pose', Pose, callback=pose_seperator)
    pose = Twist()
    
    while not rospy.is_shutdown():
        # pose = rospy.wait_for_message(/turtle1/pose)
        sub = rospy.Subscriber('/turtle1/pose', Pose, callback=pose_seperator)

        x_delta = x_goal - x_current
        y_delta = y_goal - y_current
        angle_delta = math.atan2(y_delta,x_delta) - angle_current 
        #quarter(x_delta, y_delta)

        linear_vel = beta*math.sqrt(x_delta**2 + y_delta**2)
        angular_vel = theta*angle_delta

        pose.linear.x = linear_vel
        pose.angular.z = angular_vel

        pub.publish(pose)

if __name__ == '__main__':
    try : main()
    except rospy.ROSInterruptException : pass