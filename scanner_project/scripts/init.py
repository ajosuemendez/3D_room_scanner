import roslaunch
import rospy
from std_msgs.msg import String
from std_srvs.srv import Empty

import subprocess

# class ScanInit:
#     def __init__(self):
#         #self.cp2_subscriber = rospy.Subscriber("/camera/depth/points", PointCloud2, self.show_total_cl_points)
#         self.start = False
#         self.start_calback = rospy.Subscriber("/start_cmd", String, self.start_callback)
#
#     def run(self):
#         if self.start:
#             uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
#             roslaunch.configure_logging(uuid)
#
#             cli_args = ['/opt/ros/noetic/share/realsense2_camera/launch/rs_rtabmap.launch',
#                         'args:="-d --Mem/UseOdomGravity true --Optimizer/GravitySigma 0.3"',
#                         'odom_topic:=/t265/odom/sample',
#                         'frame_id:=t265_link',
#                         'rgbd_sync:=true',
#                         'depth_topic:=/d400/aligned_depth_to_color/image_raw',
#                         'rgb_topic:=/d400/color/image_raw',
#                         'camera_info_topic:=/d400/color/camera_info',
#                         'approx_rgbd_sync:=false',
#                         'visual_odometry:=false']
#
#             roslaunch_args = cli_args[1:]
#
#
#             roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]
#
#             parent = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)
#
#             parent.start()
#
#             rospy.loginfo("started")
#
#             try:
#               parent.spin()
#             finally:
#               # After Ctrl+C, stop all nodes from running
#               parent.shutdown()
#
#     #TOPICS SUBSCRIBERS
#     def start_callback(self, msg):
#         print("sadasds")
#         self.start = True
#
#
# if __name__ == '__main__':
#     rospy.init_node('init_node')
#     ScanInit()
#     rospy.spin()
#

def start_node_direct():
    """
    Does work as well from service/topic callbacks directly using rosrun
    """
    package1 = 'realsense2_camera'
    node_name1 = 'rs_d400_and_t265.launch'


    package2 = 'rtabmap_ros'
    node_name2 = 'rtabmap.launch'
    args = 'args:="-d --Mem/UseOdomGravity true --Optimizer/GravitySigma 0.3" odom_topic:=/t265/odom/sample frame_id:=t265_link rgbd_sync:=true depth_topic:=/d400/aligned_depth_to_color/image_raw rgb_topic:=/d400/color/image_raw camera_info_topic:=/d400/color/camera_info approx_rgbd_sync:=false visual_odometry:=false'

    command = "roslaunch {0} {1}".format(package1, node_name1)
    command2 = "roslaunch {0} {1} {2}".format(package2, node_name2, args)
    # print(command)

    p = subprocess.Popen(command, shell=True)
    p2 = subprocess.Popen(command2, shell=True)

    state = p.poll()
    if state is None:
        rospy.loginfo("process is running fine")
    elif state < 0:
        rospy.loginfo("Process terminated with error")
    elif state > 0:
        rospy.loginfo("Process terminated without error")

    state = p2.poll()
    if state is None:
        rospy.loginfo("process is running fine")
    elif state < 0:
        rospy.loginfo("Process terminated with error")
    elif state > 0:
        rospy.loginfo("Process terminated without error")



# def start_node():
#     """
#     Does not work if called from service/topic callbacks due to main signaling issue
#     """
#     package = 'YOUR_PACKAGE'
#     launch_file = 'YOUR_LAUNCHFILE.launch'
#     uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
#     roslaunch.configure_logging(uuid)
#     launch_file = os.path.join(rospkg.RosPack().get_path(package), 'launch', launch_file)
#     launch = roslaunch.parent.ROSLaunchParent(uuid, [launch_file])
#     launch.start()





def controll_callback(msg):
    # print("fundsa")
    if msg.data == "init":
        print("init node...")
        start_node_direct()
        return

    if msg.data == "start":
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

        rospy.wait_for_service('/rtabmap/resume')
        service_conn = rospy.ServiceProxy('/rtabmap/resume', Empty)
        try:
            service_conn()
            print("resume scan...")
        except rospy.ServiceException as exc:
            print("Service did not process request: " + str(exc))

        return

if __name__ == "__main__":
    rospy.init_node('init_node', anonymous=True)
    service = rospy.Subscriber('/start_cmd', String, controll_callback)
    rospy.spin()
