import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Twist

class Odometry:

    def callback(msg):
        print(msg)

    odom_pub = rospy.Subscriber("/t265/odom/sample", Odometry, callback)


if __name__ == '__main__':
    rospy.init_node('odom_subscriber') 
    Odometry()
    rospy.spin()

