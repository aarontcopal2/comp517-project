# import the threading module
import threading
import time
from node import Node
import json

class PeerClient(threading.Thread):
	def __init__(self, host_ip, host_port, host_id, debug=False):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.host_port = host_port
		self.host_id = host_id
		self.debug = debug
		self.node = Node(host_ip, host_port, host_id, self.node_callback)
		print("P2PCommunication server started, host: "+ host_ip + " port: " + str(host_port) + " id: " + str(host_id))

	def run(self):
		self.node
		self.node.debug = self.debug
		self.node.start()

	def stop(self):
		self.node.stop()

	def connect_with_node(self, node_ip, node_port):
		self.node.connect_with_node(node_ip, node_port)
	
	def connect_with_master_node(self, node_ip, node_port):
		self.connect_with_node(node_ip, node_port)
		self.node.print_connections()
		time.sleep(5)
		self.get_all_nodes_from_master()

	def send_to_node(self, n, data):
		self.node.send_to_node(n, data)

	def send_to_all_nodes(self, data, exclude=[]):
		self.node.send_to_nodes(data, exclude)
	
	def check_node_message(self, from_node, data):
		if data['message'] == "send_all_nodes_data" :
			
			s = self.node.nodes_inbound
			s += self.node.nodes_outbound
			j = {"message": str(s)}
			self.send_to_node(from_node.id, json.dumps(j))

	def get_all_nodes_from_master(self):
		self.send_to_node("1", '{"message": "send_all_nodes_data"}')

	def node_callback(self, event, node, connected_node, data):
		try:
			if event == "node_message": 
				self.check_node_message(connected_node, data)
		except Exception as e:
			print(e)