# import the threading module
import threading
import time
from node import Node
from nodeconnection import NodeConnection
import json

class PeerClient(threading.Thread):
	msg = {"message":"", "value":""}
	send_all_nodes_msg = "send_all_nodes_data"
	get_all_nodes_msg = "get_all_nodes_data"
	master_node_id = 1

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
		n=str(n)
		self.node.send_to_node(n, json.dumps(data))

	def send_to_all_nodes(self, data, exclude=[]):
		self.node.send_to_nodes(json.dumps(data), exclude)
	
	def check_node_message(self, from_node, data):
		data = json.loads(data)
		if data['message'] == PeerClient.send_all_nodes_msg :
			s = self.node.nodes_inbound
			s += self.node.nodes_outbound
			print(s)
			s = [{"host": node.connected_node_host, "port": node.connected_node_port} for node in s ]
			msg = PeerClient.msg
			msg['message'] = PeerClient.get_all_nodes_msg 
			msg['value'] = str(s)
			self.send_to_node(from_node.id, json.dumps(msg))
		elif data['message'] == PeerClient.get_all_nodes_msg:
			node_list = eval(data['value'])
			for node in node_list:
				self.connect_with_node(node['host'], node['port'])

	def get_all_nodes_from_master(self):
		msg = {}
		msg['message'] = PeerClient.send_all_nodes_msg
		self.send_to_node(PeerClient.master_node_id, json.dumps(msg))

	def node_callback(self, event, node, connected_node, data):
		try:
			if event == "node_message": 
				self.check_node_message(connected_node, data)
		except Exception as e:
			print("incorrect msg from peer node: " + node.id)
			print(e)