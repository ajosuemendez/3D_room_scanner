#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from std_srvs.srv import SetBool

class CloudPoints:
    def __init__(self):
        #self.cp2_subscriber = rospy.Subscriber("/camera/depth/points", PointCloud2, self.show_total_cl_points)
        self.update_clp = rospy.Subscriber("/d400/depth/color/points", PointCloud2, self.update_clp)
        self.get_total_points_service = rospy.Service("/get_total_points", SetBool, self.show_total_cl_points)
        self.get_current_points_service = rospy.Service("/get_current_points", SetBool, self.show_coordinates)
        self.current_clp = None

    #TOPICS SUBSCRIBERS
    def update_clp(self, msg):
        self.current_clp = list(point_cloud2.read_points(msg, skip_nans=True, field_names = ("x", "y", "z")))


    ##SERVICES
    def show_total_cl_points(self, req):
        if self.current_clp and req.data:
            num_points = np.shape(self.current_clp)[0]
            print("Number of Points:", num_points)
            return True, "Successful"
        return False, "Failed to get Total amount of points in the cloud"

    def show_coordinates(self, req):
        #x, y, z = cloud_points[:,0], cloud_points[:,1], cloud_points[:,2]
        if req.data:
            for index, point in enumerate(self.current_clp):
                print(f"point number:{index} with coordinates: x={point[0]}, y={point[1]}, z={point[2]}")
                print("---------------------------")

            return True, "Successful"
        return False, "Failed to dispaly point coordinates"

if __name__ == '__main__':
    rospy.init_node('clp_node')
    CloudPoints()
    rospy.spin()
