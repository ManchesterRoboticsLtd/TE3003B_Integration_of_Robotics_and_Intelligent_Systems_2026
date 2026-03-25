<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/ManchesterRoboticsLtd/TE3003B_Integration_of_Robotics_and_Intelligent_Systems/blob/main/Misc/Logos/Logotipo%20Vertical%20Bco_Transparente.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/ManchesterRoboticsLtd/TE3003B_Integration_of_Robotics_and_Intelligent_Systems/blob/main/Misc/Logos/Logotipo%20Vertical%20Azul%20transparente.png">
  <img alt="Shows ITESM logo in black or white." width="160" align="right">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/ManchesterRoboticsLtd/TE3003B_Integration_of_Robotics_and_Intelligent_Systems/blob/main/Misc/Logos/MCR2_Logo_White.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/ManchesterRoboticsLtd/TE3003B_Integration_of_Robotics_and_Intelligent_Systems/blob/main/Misc/Logos/MCR2_Logo_Black.png">
  <img alt="Shows MCR2 logo in black or white." width="150" align="right">
</picture>

---
---
# TE3003B: Integration of Robotics and Intelligent Systems

  ## Introduction
   * This course, developed by Manchester Robotics ltd. (MCR2), aims to provide students with understanding of modern autonomous systems.
   * This course is divided into ten sessions, carefully designed for the user to learn about the problems of localisation and provide students with an overview on main topics encountered in autonomous systems field such as localization techniques, navigation, and intelligent path-planning.
   * This course will be based on challenges to make the student aware of the problems faced during the implementation of advanced intelligent algorithms in robotics.
   * This branch contains all the presentations, activities and files required for the “TE3003B: Integration of Robotics and Intelligent Systems” course of the Tec de Monterrey.
   * This repository is organised by sessions, each subfolder contains all the neccesary files for each one of the activities of this course.

   
## General Information
* Duration: 10 Weeks
* Classes: TBD
* Starts: TBD
* Ends: TBD
* ZOOM Link Classes: TBD

## Live Sessions (Recordings)
[Class Videos Playlist](https://tecmx-my.sharepoint.com/:f:/g/personal/mario_mtz_tec_mx/IgBG0kcW2BpCTINiPetrRbYFARndmeTkQG2pKxv-bqvlws8?e=b00u7L)

[Video Recordings](https://tecmx-my.sharepoint.com/:f:/g/personal/mario_mtz_tec_mx/IgBG0kcW2BpCTINiPetrRbYFAXvLPALXlzrCuoJgWLap9r4?e=46H9qG)

## General Requirements
General requirements. Please be aware that a set of requirements especific for each session will be shown in each session subsection (Some items may be repeated).
* Computer with access to Zoom (online classes).
* Computer with Ubuntu 22.04 ROS2 Humble.
* Knowledge of ROS.
* Knowledge of Windows. 
* Basic knowledge of Ubuntu (recommended).
* Basic understanding of robotics (recommended).
* Access to a Puzzlebot Jetson/Lidar Edition. 


## Puzzlebot Firmware

*Update the firmware of the hackerboard in the following link

* [Puzzleware](https://tecmx-my.sharepoint.com/:f:/g/personal/mario_mtz_tec_mx/EuisZe1eG5xKvGpsFljJwUoBcYvHmaIm8q2_aM8XN5ETqw?e=p7kvBT)

* Download the zip file.
* Follow the instructions for your OS.

## Puzzlebot Jetson Image
* Install [Balena Etcher](https://etcher.balena.io/) to format and upload the following image to the micro SD card.
* [Jetson image option 1](https://manchesterrobotics-my.sharepoint.com/:u:/g/personal/mario_mtz_manchester-robotics_com/EVMUSVxzaepInxdKvzXnhpQBlhEpad4ZZDCQylmIlI3PlQ?e=5eqEzd) 
* [Jetson image option 2](https://www.dropbox.com/scl/fi/2ccqhr9g0u5rj15ysr93r/jetson_2gb_ubuntu20.zip?rlkey=5iq4ebmrf529t5t2jztprsvhp&dl=0)


## Weekly Sessions

  ### Week 1: Dynamical Systems
  This week will introduce the teaching team and the basics of dynamical systems.

  #### Session:
  * Course Introduction.
  *	Transforms in ROS2
  *	URDF
  *	Markers in ROS 2

  **Activity** : Modelling
  - Model a Drone in ROS 2
  
  **Mini challenge:** 
  *	Model a Puzzlebot in ROS 2 and visualise it using RVIZ.

  
  ### Week 2: Mobile Robots – Fundamentals
  This week will introduce a review of mobile robotics.
  #### Session:
  *	Kinematics for a differential drive mobile robot.
  *	Dead Reckoning (Encoder-based localisation)
  *	Point-to-point navigation.

  **Mini challenge:** 
  *	Model the kinematic model of the Puzzlebot in ROS and Visualise it in RVIZ.
  *	Move the robot using a point-to-point navigation strategy.


  ### Week 3: Probabilities in Robotics
  * Introduction to probabilities
    -	Preliminaries (Basics).
    -	Discrete random variables.
    -	Continuous random variables.
    -	Distributions (Uniform, Gaussian)
  *	Linearisation – Fundamentals
  
  **Mini challenge:**: 
  * Multi-robot plotting in ROS 2
  

  
  ### Week 4: Uncertainty in mobile robotics
  This week will introduce the concept of reactive navigation for robotics.
  #### Session:
  *	Ellipsoid of confidence.
  *	Mobile robot localisation (dead reckoning) in the presence of uncertainties
  
  
  **Mini challenge:**: 
  * Move the Puzzlebot in a straight line (open loop) from point A to point B, for a specified time. Repeat the experiment 15 to 20 times and record the position data. 
  * Turn the robot from an initial angle (open loop), for a specific time to a final angle, and record the position data. Repeat the experiment 15 to 20 times.
  * The experiment must be run with the real robot, Gazebo and kinematic simulation.

  * Multiple point navigation for the different paths designed. Repeat the experiment multiple times.

  *	Plot the confidence ellipsoid of a mobile robot. Use the multiple-point navigation.
    


  ### Week 5: Reactive navigation
  This week will introduce the concept of reactive navigation for robotics.
  
  #### Session:
  * Exteroceptive sensors.
  *	Obstacle avoidance
  *	Obstacle avoidance algorithms: 
    - Bug 0, Bug 1, Bug 2.

  **Mini challenge:**: 
  * Implementation of obstacle avoidance algorithms Bug 0 and Bug 2 in simulation (Gazebo) and with the real robot.
  

  ### Week 6: Sources of information
  This week the concept of Kalman filter will be introduced.
  
  #### Session:
  * Bayes Filter.
  *	Kalman Filter
  *	Kalman Filter for map-based localisation (2D).

  **Mini challenge:**: 
  * Implementation of obstacle avoidance algorithms Bug 0 and Bug 2 in simulation (Gazebo) and with the real robot.

  

  ### Week 7: Final Challenge
  This week the Final Challenge will be presented.
  
  #### Session:
  * Kalman Filter for map-based localisation (2D).
  *	Camera based localisation for mobile robots.
    -	Aruco markers
    -	Visual localisation of mobile robots using Aruco markers
    -	Kalman filter for map-based localisation in 3D. Kalman filter estimation by combining visual localization with encoder information.


  #### Final Challenge
  *	Mobile robots’ navigation
  *	Camera based Kalman filter localisation for the Puzzlebot. (Steps)
    1.	Multiple point navigation with obstacle avoidance. Use Dead reckoning localization.
    2.	Multiple point navigation no obstacles, using visual based localisation.
    3.	Multiple point navigation no obstacles, using Kalman filter estimation.
    4.	Multiple point navigation with obstacles, using Kalman filter estimation. 

  ### Week 8: Final Challenge
  This week will be dedicated to a Q&A session.
  
  #### Session:
  * Q&A Session.


  ### Week 9: Grading
  This week will be dedicated to a Q&A session.
  
  #### Session:
  * Grading.


    ---
## Declaration

At Manchester Robotics, we firmly believe that innovation is driven by change, so we have made it our mission to change access to educational robotics. We hope you enjoy our products and support this revolution.

So, from the team at MCR2, we would like to say 

                                                          Thank you!
                                                   {Learn, Create, Innovate};
---
  ## Disclaimer
 *THE PIECES, IMAGES, VIDEOS, DOCUMENTATION, ETC. SHOWN HERE ARE FOR INFORMATIVE PURPOSES ONLY. THE DESIGN IS PROPRIETARY AND CONFIDENTIAL TO MANCHESTER ROBOTICS LTD. (MCR2). THE INFORMATION, CODE, SIMULATORS, DRAWINGS, VIDEOS PRESENTATIONS ETC. CONTAINED IN THIS REPOSITORY IS THE SOLE PROPERTY OF MANCHESTER ROBOTICS LTD. ANY REPRODUCTION OR USAGE IN PART OR AS A WHOLE WITHOUT THE WRITTEN PERMISSION OF MANCHESTER ROBOTICS LTD. IS STRICTLY PROHIBITED*

*THIS WEBSITE MAY CONTAIN LINKS TO OTHER WEBSITES OR CONTENT BELONGING TO OR ORIGINATING FROM THIRD PARTIES OR LINKS TO WEBSITES AND FEATURES IN BANNERS OR OTHER ADVERTISING. SUCH EXTERNAL LINKS ARE NOT INVESTIGATED, MONITORED, OR CHECKED FOR ACCURACY, ADEQUACY, VALIDITY, RELIABILITY, AVAILABILITY OR COMPLETENESS BY US.*

*WE DO NOT WARRANT, ENDORSE, GUARANTEE, OR ASSUME RESPONSIBILITY FOR THE ACCURACY OR RELIABILITY OF ANY INFORMATION OFFERED BY THIRD-PARTY WEBSITES LINKED THROUGH THE SITE OR ANY WEBSITE OR FEATURE LINKED IN ANY BANNER OR OTHER ADVERTISING.*
