#!/usr/bin/env python

import rospy
import os
import signal
import numpy as np
import rosnode
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from std_msgs.msg import String
from std_srvs.srv import Empty
import pcl_ros

import subprocess




class PointCloudFileGenerator:

    def clean_shutdown(self):
        if self.p is not None:
            self.p.terminate()
            self.p.kill()
        if self.p2 is not None:
            self.p2.terminate()
            self.p2.kill()
        

    def __init__(self):
        self.pointc_cloud_map_subscriber = rospy.Subscriber("/rtabmap/cloud_map", PointCloud2, self.update_point_cloud_callback)
        self.web_control = rospy.Subscriber('/start_cmd', String, self.controll_callback)
        #rospy.on_shutdown(self.clean_shutdown)
        self.p = None
        self.p2 = None
        self.init_camera()

    def update_point_cloud_callback(self, msg):
        self.current_point_cloud_map = list(point_cloud2.read_points(msg, skip_nans=True, field_names = ("x", "y", "z")))
        num_points = np.shape(self.current_point_cloud_map)[0]
        print(num_points)

    def init_camera(self):
        package1 = 'realsense2_camera'
        node_name1 = 'rs_d400_and_t265.launch'


        package2 = 'rtabmap_ros'
        node_name2 = 'rtabmap.launch'
        args = 'args:="-d --Mem/UseOdomGravity true --Optimizer/GravitySigma 0.3" odom_topic:=/t265/odom/sample frame_id:=t265_link rgbd_sync:=true depth_topic:=/d400/aligned_depth_to_color/image_raw rgb_topic:=/d400/color/image_raw camera_info_topic:=/d400/color/camera_info approx_rgbd_sync:=false visual_odometry:=false'

        command = "roslaunch {0} {1}".format(package1, node_name1)
        command2 = "roslaunch {0} {1} {2}".format(package2, node_name2, args)

        self.p = subprocess.Popen(command, shell=True)
        self.p2 = subprocess.Popen(command2, shell=True)

        state = self.p.poll()
        if state is None:
            rospy.loginfo("process is running fine")
        elif state < 0:
            rospy.loginfo("Process terminated with error")
        elif state > 0:
            rospy.loginfo("Process terminated without error")

        state2 = self.p2.poll()
        if state2 is None:
            rospy.loginfo("process is running fine")
        elif state2 < 0:
            rospy.loginfo("Process terminated with error")
        elif state2 > 0:
            rospy.loginfo("Process terminated without error")


    def controll_callback(self, msg):

        if msg.data == "start":

            rospy.wait_for_service('/rtabmap/resume')
            service_conn = rospy.ServiceProxy('/rtabmap/resume', Empty)
            try:
                service_conn()
                print("resume scan...")
            except rospy.ServiceException as exc:
                print("Service did not process request: " + str(exc))

        
            rospy.wait_for_service('/rtabmap/reset')
            service_conn = rospy.ServiceProxy('/rtabmap/reset', Empty)
            try:
                service_conn()
                print("reset scan...")
            except rospy.ServiceException as exc:
                print("Service did not process request: " + str(exc))

            return

        if msg.data == "stop":

            rospy.wait_for_service('/rtabmap/pause')
            service_conn = rospy.ServiceProxy('/rtabmap/pause', Empty)
            try:
                service_conn()
                print("pausing scan...")
            except rospy.ServiceException as exc:
                print("Service did not process request: " + str(exc))

            self.save_point_cloud_file()
            self.convert_to_pyl()

            rospy.wait_for_service('/rtabmap/resume')
            service_conn = rospy.ServiceProxy('/rtabmap/resume', Empty)
            try:
                service_conn()
                print("resume scan...")
            except rospy.ServiceException as exc:
                print("Service did not process request: " + str(exc))

            return

        return
    
    def save_point_cloud_file(self):

        package = 'pcl_ros'
        node_name = 'pointcloud_to_pcd'
        input = 'input:=/rtabmap/cloud_map'
        prefix = '_prefix:=/home/scrumpractice/catkin_ws/src/scanner_project/web/pcd/test_'

        command = "rosrun {0} {1} {2} {3}".format(package, node_name, input, prefix)

        self.p4 = subprocess.Popen(command, shell=True)
        
        state = self.p4.poll()
        if state is None:
            rospy.loginfo("process is running fine")
        elif state < 0:
            rospy.loginfo("Process terminated with error")
        elif state > 0:
            rospy.loginfo("Process terminated without error")

        print("ashdasd")

        rate = rospy.Rate(1)
        rate.sleep()
        self.kill_node_pc_to_pcd()


    def kill_node_pc_to_pcd(self):
        for node in rosnode.get_node_names():
            print("current node:", node)
            if node[:18] == "/pointcloud_to_pcd":
                print(f'rosnode kill {node}')
                os.system(f'rosnode kill {node}')
                self.p4.terminate()
                self.p4.kill()

        

    def convert_to_pyl(self):
        print("converting file")
        onlyfiles = [f for f in os.listdir("/home/scrumpractice/catkin_ws/src/scanner_project/web/pcd/") if os.path.isfile(os.path.join("/home/scrumpractice/catkin_ws/src/scanner_project/web/pcd/", f))]
        print(onlyfiles)
        for f in onlyfiles:
            if f[-1] == "d":
                #os.system(f"pcl_pcd2ply /home/scrumpractice/catkin_ws/src/scanner_project/web/pcd/{f} /home/scrumpractice/catkin_ws/src/scanner_project/web/pcd/{f}.ply")
                os.system(f"pcl_pcd2ply /home/scrumpractice/catkin_ws/src/scanner_project/web/pcd/{f} /home/scrumpractice/scrum_week_api/public/models/ply/{f}.ply")
                os.system(f"rm /home/scrumpractice/catkin_ws/src/scanner_project/web/pcd/{f}")
                #os.system(f"mv /home/scrumpractice/catkin_ws/src/scanner_project/web/pcd/{f}.ply" "/home/scrumpractice/scrum_week_api/public/models/ply/{f}.ply")
                #os.system(f"cp /home/scrumpractice/catkin_ws/src/scanner_project/web/pcd/{f}.ply /home/scrumpractice/Dokumente/scrum-week-web/dist/client/{f}.ply")



if __name__ == '__main__':
    rospy.init_node('point_cloud_file_generator')
    PointCloudFileGenerator()
    
    rospy.spin()
