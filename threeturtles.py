#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
import random

def create_turtle(x, y, theta, name):
    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', Spawn)
    spawner(x, y, theta, name)

def move_turtles(turtle_names):
    turtle_names.insert(0, "turtle1")
    publishers = [rospy.Publisher(f'/{name}/cmd_vel', Twist, queue_size=10) for name in turtle_names]
    rate = rospy.Rate(10)
    
    counter = 0
    while not rospy.is_shutdown():
        twist = Twist()
        twist.linear.x = random.randrange(-20, 20, 2)
        twist.angular.z = 0.0
        publishers[counter].publish(twist)
        rate.sleep()
        
        twist.linear.x = 0.0
        twist.angular.z = random.randrange(-20, 20, 2)
        publishers[counter].publish(twist)
        rate.sleep()

        if(counter >= len(publishers)-1):
            counter = 0
        else:
            counter = counter + 1

if __name__ == '__main__':
    try:
        rospy.init_node('turtle_spawner')
        
        turtle_names = ["Dogobot", "Catobot"]
        for name in turtle_names:
            x = random.randrange(1, 10, 2)
            y = random.randrange(1, 10, 2)
            theta = 0
            create_turtle(x, y, theta, name)
        
        move_turtles(turtle_names)
    except rospy.ROSInterruptException:
        pass