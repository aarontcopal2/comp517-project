#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# This example show how to derive a own Node class (MyOwnPeer2PeerNode) from p2pnet.Node to implement your own Node   #
# implementation. See the MyOwnPeer2PeerNode.py for all the details. In that class all your own application specific  #
# details are coded.                                                                                                  #
#######################################################################################################################

import sys
import os
import time
sys.path.insert(0, '..') # Import the files where the modules are located

from client import PeerClient

def stop_node(node):
	if node is not None:
		node.stop()

def main():
	peer_node = None
	try:

		host_ip = sys.argv[1].split(':')[0]
		host_port = int(sys.argv[1].split(':')[1])
		
		# host_ip = "127.0.0.1"
		# host_port = 8001

		host_id = int(sys.argv[2])
		# host_id = 2
		
		# master_ip = sys.argv[3].split(':')[0]
		# master_port = int(sys.argv[3].split(':')[1])

		master_ip = "127.0.0.1"
		master_port = 8000

		peer_node = PeerClient(host_ip, host_port, host_id , True)
		peer_node.start()
		time.sleep(5)
		peer_node.connect_with_master_node(master_ip, master_port)

		while 1:
			s = input()
			if s == 'q' :
				stop_node(peer_node)
			os._exit(1)

	except Exception as e:
		raise e
		stop_node(peer_node)
		os._exit(1)

if __name__ == "__main__":
	main()
