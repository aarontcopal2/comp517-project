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
import traceback
import pyodbc

sys.path.insert(0, '..') # Import the files where the modules are located

from client import PeerClient


databaseName = 'master'
username = 'comp517'
password = 'comp517'
server = 'tcp:127.0.0.1;PORT=1433'
driver= '{ODBC Driver 17 for SQL Server}'
CONNECTION_STRING = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+databaseName+';UID='+username+';PWD='+ password

conn = pyodbc.connect(CONNECTION_STRING)
cursor = conn.cursor()


def stop_node(node):
	if node is not None:
		node.stop()

def get_master_node():
	cursor = conn.cursor()
	query = "SELECT * FROM leader_node"
	cursor.execute(query);
	res = cursor.fetchone()[1].split(":")
	cursor.close()
	return res

def main():
	peer_node = None
	try:

		host_ip = sys.argv[1].split(':')[0]
		host_port = int(sys.argv[1].split(':')[1])
		
		host_id = int(sys.argv[2])

		[master_ip, master_port] = get_master_node()

		peer_node = PeerClient(host_ip, host_port, host_id , False)
		peer_node.start()
		time.sleep(5)
		peer_node.connect_with_master_node(master_ip, int(master_port))

		while 1:
			s = input()
			if s == 'q' :
				stop_node(peer_node)
			os._exit(1)

	except Exception as e:
		traceback.print_exc()
		stop_node(peer_node)
		os._exit(1)

if __name__ == "__main__":
	main()
