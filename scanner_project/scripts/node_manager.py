#!/usr/bin/env python
import rospy
import os
import signal
import rosnode
import subprocess
from std_msgs.msg import String


class NodeManager:

    def __init__(self):
        self.start_node_subscriber = rospy.Subscriber("/start_cmd", String, self.start_node_callback)
        self.kill_node_subscriber = rospy.Subscriber("/start_cmd", String, self.kill_node_callback)
        self.node_to_kill = ""
    
    def start_node_callback(self, msg):
        if msg.data == "initialize":
            if "/point_cloud_file_generator" not in rosnode.get_node_names():
                command = "rosrun scanner_project point_cloud_file_generation.py"
                print("running rosnode")

                #subprocess.run(["/home/scrumpractice/catkin_ws/src/scanner_project/init.bash"], shell=True)
                self.p = subprocess.Popen(command, shell=True)

                state = self.p.poll()
                if state is None:
                    rospy.loginfo("process is running fine")
                elif state < 0:
                    rospy.loginfo("Process terminated with error")
                elif state > 0:
                    rospy.loginfo("Process terminated without error")
    
    def kill_node_callback(self, msg):
        if msg.data == "kill":

            for node in rosnode.get_node_names():
                print(node)
                if node[:18] == "/pointcloud_to_pcd":
                    #self.node_to_kill = node
                    os.system(f'rosnode kill {node}')

            os.system('rosnode kill /rtabmap/rgbd_sync')
            os.system('rosnode kill /d400/realsense2_camera')
            os.system('rosnode kill /rtabmap/rtabmap')
            os.system('rosnode kill /rtabmap/rtabmapviz')
            os.system('rosnode kill /t265/realsense2_camera')
            os.system('rosnode kill /t265/realsense2_camera_manager')
            os.system('rosnode kill /t265_to_d400')
            os.system('rosnode kill /d400/realsense2_camera_manager')
            os.system('rosnode kill /point_cloud_file_generator')
            #os.system(f'rosnode kill {self.node_to_kill}')


if __name__ == '__main__':
    rospy.init_node('node_manager')
    NodeManager()
    rospy.loginfo("NODE MANAGER INITIALIZED")
    rospy.spin()
