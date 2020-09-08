#! /usr/bin/env python3
import os
import asyncio
from six.moves import input
import threading
from azure.iot.device.aio import IoTHubModuleClient
from std_msgs.msg import String
import rospy
import time


class Connector(object):
    pub_string=""
    
    def __init__(self):
        self.pub = rospy.Publisher('blocked', String, queue_size=2)
        self.module_client = IoTHubModuleClient.create_from_edge_environment()
        print("Starting ROSConnector Module")
        print("Connect Client...")
        
        rospy.init_node('detection')
        print("....")
        # connect the client.
        print("Client Connected!")
        self.r = rospy.Rate(10) # 10hz
    async def input1_listener(self,module_client):
        print("starting input listener..")
        while True:
            input_message = await self.module_client.receive_message_on_input("input1")  # blocking call
            print("the data in the message received on input1 was ")
            print(input_message.data.decode("utf-8"))        #b'{"chair": 1}'
            pub_string="test2"
            self.r.sleep()
            self.pub.publish(pub_string)
            if 'person' in input_message.data.decode("utf-8") :
                print("Person detected")
                self.r.sleep()
                pub_string="detected"
                rospy.loginfo(pub_string)
                self.pub.publish(pub_string)
            else:
                print("No Person found")
                pub_string="clear"
                rospy.loginfo(pub_string)
                self.pub.publish(pub_string)
                self.r.sleep()
                
            # print("custom properties are")
            # print(input_message.custom_properties)
    async def main(self):
        await self.module_client.connect()
        
        listeners = asyncio.gather(self.input1_listener(self.module_client))
        
#         hello_str = "hello world %s" % rospy.get_time()
#         
#         pub.publish(hello_str)



# async def main():
#     # The client object is used to interact with your Azure IoT hub.
#     try: 
        
#         # define behavior for receiving an input message on input1
#         async def input1_listener(module_client):
#             print("starting input listener..")
#             while True:
#                 input_message = await module_client.receive_message_on_input("input1")  # blocking call
#                 print("the data in the message received on input1 was ")
#                 print(input_message.data)        #b'{"chair": 1}'
#                 pub.publish(input_message.data)
#                 print("custom properties are")
#                 print(input_message.custom_properties)
          

    
#         # Schedule task for listeners
#         listeners = asyncio.gather(input1_listener(module_client))
#         r.sleep()
#         # Cancel listening
#     except Exception as e: 
#         listeners.cancel()
#         # Finally, disconnect
#         await self.module_client.disconnect()
#         print("shuting down everything due to:"+ str(e))

    



if __name__ == "__main__":
    #asyncio.run(main())
    try:
        loop = asyncio.get_event_loop()
        connector=Connector()
    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
        while True:
            
            
            
            loop.run_until_complete(connector.main())
            time.sleep(3)
            
    except Exception as e: 
        print("Loop had to be closed due to:"+ str(e))
        loop.close()
        