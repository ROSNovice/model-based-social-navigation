#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import os
import rospy
import numpy as np
import math
from math import pi
import random
import time

from geometry_msgs.msg import Twist, Point, Pose
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_srvs.srv import Empty
from gazebo_msgs.srv import SpawnModel, DeleteModel

from gazebo_msgs.msg import ModelStates
from gazebo_msgs.msg import ModelState

import agent

goal_model_1_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', '..', 'turtlebot', 'turtlebot_gazebo', 'models', 'Target_1', 'model.sdf')



class Env():
    def __init__(self, is_training):

        # Simulation 仿真设置
        self.reset_proxy = rospy.ServiceProxy('gazebo/reset_simulation', Empty)
        self.unpause_proxy = rospy.ServiceProxy('gazebo/unpause_physics', Empty)
        self.pause_proxy = rospy.ServiceProxy('gazebo/pause_physics', Empty)

        self.goal_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        self.del_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)

        self.pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=1)

        threshold_goal = 0.0
        if is_training == True:
            threshold_goal = 0.5
            threshold_collision = 0.27
        else:
            threshold_goal = 0.55
            threshold_collision = 0.24

        # Agent 智能体
        self.agent_1 = agent.Agent(num=1, threshold_goal=threshold_goal, threshold_collision=threshold_collision, flag_of_social=False)

        time.sleep(1.0)

        
    # 根据num获取agent状态
    def get_agent_state(self, num):

        done = False
        arrive = False
        if num == 1:
            state_all, done, arrive = self.agent_1.get_state()

        return state_all, done, arrive

    # 根据num获取agent reward
    def get_agent_reward(self, num):
        if num == 1:
            reward, flag_ego_safety, flag_social_safety = self.agent_1._compute_reward()
        return reward, flag_ego_safety, flag_social_safety

    # reset all agent
    def get_agent_reset(self):
        self.agent_1.reset()

    # env step
    def step(self, action):
        
        self.agent_1.set_action([action[0], action[1]])

        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            self.unpause_proxy()
        except (rospy.ServiceException) as e:
            print("gazebo/unpause_physics service call failed")

        time.sleep(0.1)
        
        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            self.pause_proxy()
        except (rospy.ServiceException) as e:
            print("gazebo/pause_physics service call failed")
        
        time.sleep(0.1)


        t1 = time.time()
        state_all_1, done_1, arrive_1 = self.get_agent_state(1)
        t2 = time.time()
        # print("Step Time : {}  ms".format(round(1000*(t2-t1),2)))

        reward_1, flag_ego_safety_1, flag_social_safety_1 = self.get_agent_reward(1)

        return state_all_1, reward_1, done_1 or arrive_1


    def reset(self):
        print("=============================>  Env Reset <=============================   ", self.agent_1.cumulated_steps)
        # Reset the env

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            self.pause_proxy()
        except (rospy.ServiceException) as e:
            print("gazebo/pause_physics service call failed")
        
        time.sleep(0.1)
        
        rospy.wait_for_service('/gazebo/delete_model')
        try:
            self.del_model('target_1')
        except (rospy.ServiceException) as e:
            print("gazebo/delete_model service call failed")

        
        time.sleep(0.1)

        rospy.wait_for_service('gazebo/reset_simulation')
        try:
            self.reset_proxy()
        except (rospy.ServiceException) as e:
            print("gazebo/reset_simulation service call failed")

        time.sleep(0.05)
        # Reset robot
        self.robot_ModelState = ModelState()
        self.robot_ModelState.model_name = 'mobile_base_1'
        self.robot_ModelState.reference_frame = 'map'

        self.robot_ModelState.pose.position.x = (2.0 * random.random()) - 1.0
        self.robot_ModelState.pose.position.y = (2.0 * random.random()) - 1.0
        self.robot_ModelState.pose.position.z = 0.0

        yaw = - pi / 2.0 / 2.0
        yaw = (6.28 * random.random()) - 3.14
        cos_yaw = math.cos(yaw)
        sin_yaw = math.sin(yaw)
        self.robot_ModelState.pose.orientation.x = 0.0
        self.robot_ModelState.pose.orientation.y = 0.0
        self.robot_ModelState.pose.orientation.z = sin_yaw
        self.robot_ModelState.pose.orientation.w = cos_yaw

        self.robot_ModelState.twist.linear.x = 0.0
        self.robot_ModelState.twist.angular.z = 0.0

        self.pub.publish(self.robot_ModelState)
        time.sleep(0.05)

        self.get_agent_reset()

        # Build the targets
        # 1
        # Build the target
        rospy.wait_for_service('/gazebo/spawn_sdf_model')
        try:
            goal_urdf = open(goal_model_1_dir, "r").read()
            target_1 = SpawnModel
            target_1.model_name = 'target_1'  # the same with sdf name
            target_1.model_xml = goal_urdf
            goal_model_position = Pose()
            
            mode = random.random() * 4
            if mode < 1:
                temp_x = 6.5
                temp_y = (12.0 * random.random()) - 6.0
            elif mode >= 1 and mode < 2:
                temp_x = -6.5
                temp_y = (12.0 * random.random()) - 6.0
            elif mode >= 2 and mode < 3:
                temp_x = (12.0 * random.random()) - 6.0
                temp_y = 7
            elif mode >= 3 and mode < 4:
                temp_x = (12.0 * random.random()) - 6.0
                temp_y = -7
            


            goal_model_position.position.x, goal_model_position.position.y = temp_x, temp_y
            self.agent_1.update_target((temp_x, temp_y))
            self.goal_model(target_1.model_name, target_1.model_xml, 'namespace', goal_model_position, 'world')
            # print('=============    reset  Target reset for agent_1!')
        except (rospy.ServiceException) as e:
            print("/gazebo/failed to build the target_1")
        
        time.sleep(0.5)

        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            self.unpause_proxy()
        except (rospy.ServiceException) as e:
            print("gazebo/unpause_physics service call failed")


        time.sleep(0.2)
        state_all_1, done_1, arrive_1 = self.get_agent_state(1)

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            self.pause_proxy()
        except (rospy.ServiceException) as e:
            print("gazebo/pause_physics service call failed")

        print("=============================>  Env Reset <=============================")
        return state_all_1
