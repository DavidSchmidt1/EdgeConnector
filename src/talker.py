#! /usr/bin/env python3
import os
import asyncio
from six.moves import input
import threading
from azure.iot.device.aio import IoTHubModuleClient
from std_msgs.msg import String
import rospy


class Connector(object):
    def __init__(self):
        
        self.module_client = IoTHubModuleClient.create_from_edge_environment()
        print("Starting ROSConnector Module")
        print("Connect Client...")
        self.pub = rospy.Publisher('blocked', String, queue_size=2)
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
            print(input_message.data)        #b'{"chair": 1}'
            pub.publish(input_message.data)
            print("custom properties are")
            print(input_message.custom_properties)
    async def main(self):
        print("testing main")
        await self.module_client.connect()
        listeners = asyncio.gather(self.input1_listener(self.module_client))
        self.r.sleep()




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
            
    except Exception as e: 
        print("Loop had to be closed due to:"+ str(e))
        loop.close()
        