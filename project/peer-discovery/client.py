# import the threading module
import threading
import time
import json
import os
import traceback
import sys
sys.path.insert(0, '..') # Import the files where the modules are located

from node import Node
from nodeconnection import NodeConnection
from crawler.crawler import Crawler
from pagerank.pagerank import Pagerank

class PeerClient(threading.Thread):
	msg = {"message":"", "value":""}
	send_all_nodes_msg = "send_all_nodes_data"
	get_all_nodes_msg = "get_all_nodes_data"
	crawl_msg = "crawl"
	pagerank_msg = "pagerank"
	master_node_id = 1
	output_dir = "./output"

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
	
	def connect_with_nodes(self, data):
		node_list = eval(data['value'])
		for node in node_list:
			self.connect_with_node(node['host'], node['port'])
	
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

	def get_all_connected_nodes(self):
		s = self.node.nodes_inbound
		s += self.node.nodes_outbound 
		return s
	
	def send_info_abt_all_nodes(self, to_node, data):
		s = self.get_all_connected_nodes()
		s = [{"host": node.connected_node_host, "port": node.connected_node_port} for node in s ]
		msg = PeerClient.msg
		msg['message'] = PeerClient.get_all_nodes_msg 
		msg['value'] = str(s)
		self.send_to_node(to_node.id, json.dumps(msg))
			
	def check_node_message(self, from_node, data):
		data = json.loads(data)
		if data['message'] == PeerClient.send_all_nodes_msg :
			self.send_info_abt_all_nodes(from_node, data)
		elif data['message'] == PeerClient.get_all_nodes_msg:
			self.connect_with_nodes(data)
		elif data['message'] == PeerClient.crawl_msg:
			self.crawl(data['value'])
		elif data['message'] == PeerClient.pagerank_msg:
			self.pagerank(data['value'])
		
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
			traceback.print_exception()

	# pagerank the crawl output  
	def pagerank(self, crawl_output_file):
		crawl_output = {}
		crawl_output_list = []
		op_file = PeerClient.output_dir + "/" + self.node.id + ".done"
		if os.path.exists(op_file):
			os.remove(op_file)
		
		with open(crawl_output_file, 'r') as f:
			crawl_output = json.loads(f.read())
		
		crawl_output_list = list(crawl_output.keys())

		tot_lines = len(crawl_output)
		n = len(self.get_all_connected_nodes())
		
		pagerank_input = {}
		node_range_lbound = int(tot_lines/n) * (int(self.node.id)-1)
		node_range_ubound = min(node_range_lbound + int(tot_lines/n), tot_lines) 
		

		for i in range(node_range_lbound, node_range_ubound):
			pagerank_input[crawl_output_list[i]] = crawl_output[crawl_output_list[i]]

		Pagerank(PeerClient.output_dir + "/" + self.node.id + "_pagerank_output", tot_lines, pagerank_input)
		f =  open(op_file, "w+")
				
	# crawl the input  
	def crawl(self, input_file):
		lines = []
		op_file = PeerClient.output_dir + "/" + self.node.id + ".done"
		if os.path.exists(op_file):
			os.remove(op_file)
		with open(input_file, 'r') as f:
			lines = f.readlines()
		tot_lines = len(lines)
		n = len(self.get_all_connected_nodes())

		webpages=[]
		node_range_lbound = int(tot_lines/n) * (int(self.node.id)-1)
		node_range_ubound = min(node_range_lbound + int(tot_lines/n), tot_lines) 

		for i in range(node_range_lbound, node_range_ubound):
			webpages.append(lines[i])

		c = Crawler(webpages, PeerClient.output_dir + "/" + self.node.id + "_crawl_output.json")
		c.crawl()
		f =  open(op_file, "w+")