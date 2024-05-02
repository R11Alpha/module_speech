#!/usr/bin/env python
# coding=utf-8
import sys
import rospy  # ROS
from basicmodutil_pkg import commBM # Basic module communication functions
from std_msgs.msg import String, Bool, Empty

class BasicModuleSpeech:
    def __init__(self,bm_name):
        #Name of the basic module this node will serve as bridge
        self.__basic_mod_name = bm_name

        #comm-topics
        top_comm_pub  = "/function/output"
        top_event_pub = "/event/output"
        top_comm_sub  = "/master/output"

        #comm pub & sub
        self.__comm_pub = rospy.Publisher(top_comm_pub,String,queue_size=1)
        self.__event_pub = rospy.Publisher(top_event_pub,String,queue_size=1)
        self.__comm_sub = rospy.Subscriber(top_comm_sub,String,self.__comm_cb)

        # Talking and status topics
        talk_topic = rospy.get_param('talk_topic','/pocket_listener/talk')
        talk_status_topic = rospy.get_param('talk_status_topic','/pocket_listener/status')
        whisper_output_topic = '/module_speech/whisper_output'

        # other subs and pubs
        self.talk_pub = rospy.Publisher(talk_topic,String,queue_size=1)
        self.status_sub = rospy.Subscriber(talk_status_topic,String,self.talk_status_cb)
        self.whisper_sub = rospy.Subscriber(whisper_output_topic,String,self.event_cb)

        # State variables
        self.current_function = None
        self.waitForwaitForCommandEnd = False
        self.is_talking = False

        #DISPLAY IN CONSOLE THE BRIDGE INFO
        rospy.loginfo("BASIC-MODULE")
        rospy.loginfo("\t%s",bm_name)
        rospy.loginfo("COMM-TOPICS")
        rospy.loginfo("\t%s",top_comm_pub)
        rospy.loginfo("\t%s",top_event_pub)
        rospy.loginfo("\t%s",top_comm_sub)
        rospy.loginfo("######################################")

    def __comm_cb(self,data):
        #Parse the function-invocation message into a dictionary
        bm, func, msgs = commBM.readFunCall(data.data)

        #Check if this basic module is being requested
        if(bm == self.__basic_mod_name):
            #Debug info
            rospy.loginfo("----------------------------------")
            rospy.loginfo('COMM_CB')
            rospy.loginfo('BASIC MODULE')
            rospy.loginfo("\t%s",bm)
            rospy.loginfo('FUNCTION')
            rospy.loginfo("\t%s",func)
            rospy.loginfo('DATA')
            print(msgs)
            rospy.loginfo("----------------------------------")
            if(func == 'say'):
                self.say(msgs)

    def talk_status_cb(self,msg):
        if msg.data == 'ready':
            # To start listening spoken commands again
            self.is_talking = False

            # Return params after the robot finished speaking
            if self.current_function == 'say' and self.waitForwaitForCommandEnd:
                self.current_function = None
                out_params = []
                names = []
                msg_str = commBM.writeMsgFromRos(out_params, names)
                out_msg = String(msg_str)
                self.__comm_pub.publish(out_msg)

    def event_cb(self,msg):
        if not self.is_talking:
            # Publish as a stop-command event
            mod_name = self.__basic_mod_name
            event_name = 'spokenCommand'
            values = [String(msg.data)]
            names = ['command']
            json_str = commBM.writeEventFromRos(mod_name,event_name,values,names)
            self.__event_pub.publish(String(json_str))

    def say(self,msgs):
        if self.current_function == None:
            # To avoid listening spoken-command events
            self.is_talking = True

            # Publish the statement the robot will utter
            command = msgs[0].data
            wait_end = msgs[1].data
            self.current_function = 'say'
            self.waitForwaitForCommandEnd = wait_end
            self.talk_pub.publish(String(command))

            # Immediate response
            if not wait_end:
                self.current_function = None
                out_params = []
                names = []
                msg_str = commBM.writeMsgFromRos(out_params, names)
                out_msg = String(msg_str)
                self.__comm_pub.publish(out_msg)

def main(args):
	basic_module_name = 'module_speech'
	rospy.init_node(basic_module_name, anonymous=False)
	BasicModuleSpeech(basic_module_name)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")

if __name__ == '__main__':
	main(sys.argv)
