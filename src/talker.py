#! /usr/bin/env python3
from azure.iot.device.aio import IoTHubModuleClient
import rospy
import json
import time
import os
import sys
import asyncio
from std_msgs.msg import String


# class ShareModule(object):
#     def __init__(self):
#         self.data=""
#     async def Grabber(self):
#         try:
#             print("Starting Output Grabber")

#             # The client object is used to interact with your Azure IoT hub.
           

#             # define behavior for receiving an input message on input1
#             async def input1_listener(self,module_client):
                
                

#             # define behavior for halting the application
#             def stdin_listener():
#                 try:
#                     selection = input("Press Q to quit\n")
#                     if selection == "Q" or selection == "q":
#                         print("Quitting...")
#                         break
#                 except:
#                     time.sleep(10)

#         # Schedule task for C2D Listener
#             listeners = asyncio.gather(input1_listener(module_client))

#             print( "The sample is now waiting for messages. ")

#         # Run the stdin listener in the event loop
#             loop = asyncio.get_event_loop()
#             user_finished = loop.run_in_executor(None, stdin_listener)

#         # Wait for user to indicate they are done listening for messages
#             await user_finished

#         # Cancel listening
#             listeners.cancel()

#         # Finally, disconnect
#             await module_client.disconnect()

#         except Exception as e:
#             print ( "Unexpected error %s " % e )
#             raise
#     def returner():
#         return self.data

if __name__ == "__main__":
    module_client = IoTHubModuleClient.create_from_edge_environment()
    try:
        pub = rospy.Publisher('blocked', String, queue_size=2)
        rospy.init_node('detection')
        r = rospy.Rate(10) # 10hz
        data="test"
        # connect the client.
        module_client.connect()
    # If using Python 3.7 or above, you can use following code instead:
    # asyncio.run(main())
        while not rospy.is_shutdown():
            print("taking output to data var")
            input_message = module_client.receive_message_on_input("input1")  # blocking call
            print(input_message.data)
            data=input_message.data
            pub.publish(data)
            r.sleep()
    except Exception as e:
        print ( "Unexpected error %s " % e )
        module_client.disconnect()
        raise