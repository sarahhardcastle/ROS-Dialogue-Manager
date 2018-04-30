# ROS-Dialogue-Manger

COMMUNICATING WITH A VIRTUAL ROBOT VIA NATURAL LANGUAGE
=======================================================

This project was made as part of my dissertation, investigating spoken communication between a user and robot. 

To run:
-------
1) Ensure ROS and Gazebo are installed

2) To use Google Speech API export GOOGLE/_APPLICATION/_CREDENTIALS with the address of your credentials

3) If using turtlebot3 export TURTLEBOT3_MODEL=model with model being either burger or waffle

4) Run in seperate terminals:
    - roscore (Must be run first)
    - roslaunch turtlebot3_gazebo turtlebot3_world.launch (Or another launch file of your choosing)
    - rosrun dialogue_manager dialogue_manager.py
    - rosrun dialogue_manager speech_recognition.py
    - rosrun sound_play soundplay_node.py (Required for speech generation)

5) Enter any text in the speech_recognition.py terminal, say the command then say either "exit" or "quit" to end the sentence.

This can also be used without the speech recognition element if no Google Speech API credentials are available. In this case, use
```bash
rostopic pub /speech std_msgs/String "message" 
```
to send a string directly to the dialogue manager node.

Current capabilities:
---------------------
Currently the dialogue manager node can process commands related to movement, for example "move forwards 10M" or "Turn right 90 degrees quickly".