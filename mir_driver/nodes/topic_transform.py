#!/usr/bin/env python

import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, TwistStamped, Quaternion, TransformStamped

odom_broadcaster = tf.TransformBroadcaster()

odom_pub = None
cmd_pub = None

def odom_callback(msg):
    # odom_trans = TransformStamped()
    # odom_trans.header.stamp = msg.header.stamp
    # odom_trans.header.frame_id = 'odom'
    # odom_trans.child_frame_id = 'base_footprint'

    # odom_trans.transform.translation.x = msg.pose.pose.position.x
    # odom_trans.transform.translation.y = msg.pose.pose.position.y
    # odom_trans.transform.translation.z = 0.0
    # odom_trans.transform.rotation = msg.pose.pose.orientation

    odom_broadcaster.sendTransform((msg.pose.pose.position.x,msg.pose.pose.position.y,msg.pose.pose.position.z), 
                                    (msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w),
                                    msg.header.stamp,
                                    'base_footprint',
                                    'odom')
    odom_pub.publish(msg)
    

def cmd_callback(msg):
    mir_cmd = TwistStamped()
    mir_cmd.header.frame_id = 'base_link'
    mir_cmd.header.stamp = rospy.Time.now()
    mir_cmd.twist = msg
    cmd_pub.publish(mir_cmd)
    

def main():
    global odom_pub, cmd_pub
    rospy.init_node('topic_transfrom')

    odom_pub = rospy.Publisher('odom', Odometry, queue_size=10)
    cmd_pub = rospy.Publisher('mir_cmd', TwistStamped, queue_size=10)

    rospy.Subscriber('mir_odom', Odometry, odom_callback)
    rospy.Subscriber('cmd_vel', Twist, cmd_callback)
    rospy.spin()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass