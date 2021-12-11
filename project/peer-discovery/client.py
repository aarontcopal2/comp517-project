# import the threading module
import threading
import time
import json
import os
import traceback
import sys
from node import Node
import pyodbc
from nodeconnection import NodeConnection
from crawler.crawler import Crawler
from pagerank.pagerank import Pagerank

sys.path.insert(0, '..') # Import the files where the modules are located

def sanitize_url(k):
	url = k
	if url.startswith("https://"):
		url = url[8:]
	elif url.startswith("http://"):
		url = url[7:]
	if url.startswith("www."):
		url = url[4:]
	return url

def sanitize(graph):
	return {sanitize_url(k):[sanitize_url(x) for x in graph[k]] for k in graph}

class PeerClient(threading.Thread):
	msg = {"message":"", "value":""}
	send_all_nodes_msg = "send_all_nodes_data"
	get_all_nodes_msg = "get_all_nodes_data"
	new_crawl_msg = "new_crawl"
	crawl_msg = "crawl"
	pagerank_msg = "pagerank"
	node_joined_msg = "new_node"
	node_left_msg = "node_crashed"
	new_leader_msg = "new_leader"
	master_node_id = 1
	output_dir = "./output"
	jobid = None
	databaseName = 'master'
	username = 'comp517'
	password = 'comp517'
	server = 'tcp:127.0.0.1;PORT=1433'
	driver= '{SQL Server}'
	CONNECTION_STRING = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+databaseName+';UID='+username+';PWD='+ password
	conn = pyodbc.connect(CONNECTION_STRING)


	def __init__(self, host_ip, host_port, host_id, debug=False):
		threading.Thread.__init__(self)
		self.host_ip = host_ip
		self.host_port = host_port
		self.host_id = host_id
		self.debug = debug
		self.node = Node(host_ip, host_port, host_id, self.node_callback)
		self.new_nodes_list = []
		self.new_node = 0
		self.crawl_started = 0
		print("P2PCommunication server started, host: "+ host_ip + " port: " + str(host_port) + " id: " + str(host_id))

	def run(self):
		self.node
		self.node.debug = self.debug
		self.node.start()

	def stop(self):
		self.node.stop()

	def check_if_crawl_is_done(self):
		cursor = self.conn.cursor()
		query = "SELECT * FROM crawl_done WHERE jobid=" + str(self.jobid)
		cursor.execute(query);
		res = False
		n = len(cursor.fetchall())
		m = 1+len(self.get_all_connected_nodes())
		if n==m:
			res = True
		cursor.close()
		return res

	def connect_with_node(self, node_ip, node_port):
		self.node.connect_with_node(node_ip, node_port)
	
	def connect_with_nodes(self, data):
		node_list = eval(data['value'])
		for node in node_list:
			if node['host'] != self.host_ip or node['port'] != self.host_port:
				self.connect_with_node(node['host'], node['port'])
		print("connected with all nodes: " + str(node_list))
	
	def connect_with_master_node(self, node_ip, node_port):
		self.connect_with_node(node_ip, node_port)
		self.node.print_connections()
		self.get_all_nodes_from_master()


	def send_to_node(self, n, data):
		n=str(n)
		self.node.send_to_node(n, json.dumps(data))

	def send_to_all_nodes(self, data, exclude=[]):
		self.node.send_to_nodes(json.dumps(data), exclude)

	def get_all_connected_nodes(self):
		s = self.node.nodes_inbound
		s.update(self.node.nodes_outbound) 
		return s

	def node_disconnected(self, disconnected_node):
		if self.crawl_started == 1:
			self.new_node = -1
			self.new_nodes_list.append(disconnected_node)

		if int(disconnected_node.id) == 1 and self.get_rank() == 0:
			new_leader_ip = self.host_ip + ':' + str(self.host_port)
			msg = PeerClient.msg
			msg['message'] = PeerClient.new_leader_msg
			msg['value'] = new_leader_ip
			self.send_to_all_nodes(json.dumps(msg))
			cursor = self.conn.cursor()
			cursor.execute("UPDATE leader_node set master_ip='" + new_leader_ip + "'")
			self.conn.commit()
			cursor.close()	

	def node_connected(self, connected_node):
		if self.crawl_started == 1:
			self.new_node = 1
			self.new_nodes_list.append(connected_node)
	
	def send_info_abt_all_nodes(self, to_node, data):
		s = self.get_all_connected_nodes()
		s = [{"host": node.connected_node_host, "port": node.connected_node_port} for node in s ]
		msg = PeerClient.msg
		msg['message'] = PeerClient.get_all_nodes_msg 
		msg['value'] = str(s)
		self.send_to_node(to_node.id, json.dumps(msg))
		if self.crawl_started == 1:
			self.new_nodes_list.append(to_node.id)
			self.new_node = 1
			msg['message'] = PeerClient.new_crawl_msg 
			msg['value'] = self.jobid
			self.send_to_node(to_node.id, json.dumps(msg))
			
	def check_node_message(self, from_node, data):
		data = json.loads(data)
		print("message from node: " + str(from_node.host) + ":" + str(from_node.port) + " :" + str(data))
		if data['message'] == PeerClient.send_all_nodes_msg :
			self.send_info_abt_all_nodes(from_node, data)
		elif data['message'] == PeerClient.get_all_nodes_msg:
			self.connect_with_nodes(data)
		elif data['message'] == PeerClient.crawl_msg:
			self.crawl(data['value'])
		elif data['message'] == PeerClient.new_crawl_msg:
			self.new_node = 1
			self.crawl(data['value'], 1)
		elif data['message'] == PeerClient.pagerank_msg:
			self.pagerank(data['value'])
		elif data['message'] == PeerClient.node_joined_msg:
			self.new_node = 1
			self.new_nodes_list.append(data['value'])
		elif data['message'] == PeerClient.new_leader_msg:
			print("new leader elected with ip:" + data['value'])

	def get_all_nodes_from_master(self):
		msg = {}
		msg['message'] = PeerClient.send_all_nodes_msg
		self.send_to_node(PeerClient.master_node_id, json.dumps(msg))

	def node_callback(self, event, node, connected_node, data):
		try:
			if event == "node_message": 
				self.check_node_message(connected_node, data)
			elif event == "node_disconnected":
				self.node_disconnected(connected_node)
			elif event == "inbound_node_connected":
				self.node_connected(connected_node)
		except Exception as e:
			print("incorrect msg from peer node: " + node.id)
			print(e)
			traceback.print_exc()
			raise e

	def get_ranges(self, tot_lines, node_id):
		n = len(self.get_all_connected_nodes())+1
		node_range_lbound = int(tot_lines/n) * (node_id)
		node_range_ubound = min(node_range_lbound + int(tot_lines/n), tot_lines)
		if tot_lines < n and node_id < tot_lines:
			return node_id, node_id+1  
		return node_range_lbound, node_range_ubound

	def get_rank(self):
		connected_nodes = self.get_all_connected_nodes()
		cn_list = [int(node.id) for node in connected_nodes]
		cn_list.append(int(self.node.id))
		cn_list.sort()
		return cn_list.index(int(self.node.id))

	def get_uncommitted_work(self, node_id, jobid):
		return self.get_crawl_input(int(node_id))

	def get_new_work(self):
		new_urls = []
		for i in range(len(self.new_nodes_list)):
			new_urls.extend(self.get_uncommitted_work(self.new_nodes_list[i].id, self.jobid))	
		rank = self.get_rank()
		tot_urls = len(new_urls)
		cns = len(self.get_all_connected_nodes()) + 1
		lrange = int(tot_urls/cns)*(rank)
		urange = min(int(tot_urls/cns)*(rank+1),tot_urls)
		return new_urls[lrange : urange]

	def get_crawl_input(self, node_id, new_node=0):
		cursor = self.conn.cursor()
		cursor.execute('SELECT urls from job WHERE jobid='+str(self.jobid))
		urls = cursor.fetchone()[0]
		self.conn.commit()
		cursor.close()
		urls_list = urls.split(',')
		# print("urls = ", urls_list)
		n = 1+len(self.get_all_connected_nodes())
		return_urls = []
		if self.new_node == 1:
			n=n-1
			chunk_size = int((len(urls_list)+n-1)/n)
			for i in range(n):
				return_urls.append(urls_list[min(chunk_size*(i+1)-1, len(urls_list)-1)])
		elif self.new_node == -1:
			n = n + 1	
			chunk_size = int((len(urls_list)+n-1)/n)
			lbound = (node_id-1)*chunk_size
			ubound = min((node_id)*chunk_size, len(urls_list))
			return_urls = urls_list[lbound: ubound]
		else:
			chunk_size = int((len(urls_list)+n-1)/n)
			lbound = (node_id)*chunk_size
			ubound = min((node_id+1)*chunk_size, len(urls_list))
			return_urls = urls_list[lbound: ubound]
		
		print("crawl_input:" + str(return_urls))
		return return_urls

	def get_pagerank_input(self, node_id):
		cursor = self.conn.cursor()
		n = 1+len(self.get_all_connected_nodes())
		query = "SELECT count(*) FROM graph where jobid="+str(self.jobid)
		cursor.execute(query)
		no_urls = int(cursor.fetchone()[0])
		query = "SELECT TOP 1 id FROM graph where jobid="+str(self.jobid)
		cursor.execute(query)
		start_id = int(cursor.fetchone()[0])
		chunk_size = int((no_urls+n-1)/n)
		cursor.close()
		cursor = self.conn.cursor()
		query = "SELECT url, link FROM graph where jobid="+str(self.jobid)+" and id between " + str(start_id + node_id*chunk_size+1) + " and " + str(start_id + (node_id+1)*chunk_size)
		cursor.execute(query)
		graph = cursor.fetchall()
		graph = {x[0]:x[1] for x in graph}
		cursor.close()
		return graph, no_urls

	def set_pagerank_status_started(self, url_subset):
		cursor = self.conn.cursor()
		values = (self.jobid, ",".join(url_subset), int(self.node.id)-1, 1)
		query = "INSERT INTO pr_status(jobid, url_subset, nodeid, status) VALUES"+str(values)
		cursor.execute(query);
		self.conn.commit()
		cursor.close()

	def save_pagerank_result(self, pr):
		cursor = self.conn.cursor()
		query = "SELECT url, pr from pr where jobid="+str(self.jobid) + " and url in ('" + "','".join(pr.keys()) + "')"
		cursor.execute(query)
		res = cursor.fetchall()
		res = {x[0]:x[1] for x in res}

		for url in pr:
			if url in res:
				pr[url]+=res[url]
		query = "DELETE from PR WHERE jobid="+str(self.jobid)+" AND url in ('" + "','".join(pr.keys()) + "')"
		cursor.execute(query)
		values = [(self.jobid, k, pr[k]) for k in pr]
		values_str = ",".join([str(x) for x in values])
		query = "INSERT into PR(jobid, url, pr) values " + values_str
		cursor.execute(query)
		query = "UPDATE pr_status SET status=2 where jobid="+str(self.jobid)+" and nodeid=" + str(int(self.node.id)-1)
		self.conn.commit()
		cursor.close()

	# pagerank the crawl output  
	def pagerank(self, jobid):
		self.jobid = jobid
		node_id = int(self.node.id)-1
		graph, no_urls = self.get_pagerank_input(node_id)
		self.set_pagerank_status_started(graph.keys())
		pr = Pagerank(no_urls, graph)
		self.save_pagerank_result(pr)

	def save_crawl_result(self, graph, main_url):
		cursor = self.conn.cursor()
		for url in graph:
			cursor.execute("SELECT link from graph where jobid="+str(self.jobid) + " and url='" + url + "'")
			res = cursor.fetchone()
			if res == None or len(res)==0:
				query = "INSERT into graph(jobid, url, link, nodeid) values("+str(self.jobid) + ",'" + url + "','" + ",".join(graph[url])[:8000] + "'," + str(int(self.node.id)-1) + ");"
				cursor.execute(query)
			else:
				old_links = res[0]
				query = "UPDATE graph SET link='" + (old_links + "," + ",".join(graph[url]))[:8000] + "',nodeid=" + str(int(self.node.id)-1) + " where url='"+url+"' and jobid=" + str(self.jobid) 
				cursor.execute(query)
		values = (self.jobid, main_url, 1, int(self.node.id)-1)
		query = "INSERT INTO crawl_status(jobid, url, status, nodeid) VALUES " + str(values) 
		cursor.execute(query);
		self.conn.commit()
		cursor.close()

	def set_crawl_status_started(self, url):
		cursor = self.conn.cursor()
		values = (self.jobid, url, 1, int(self.node.id)-1)
		query = "INSERT INTO crawl_status(jobid, url, status, nodeid) VALUES "+str(values)
		cursor.execute(query);
		self.conn.commit()
		cursor.close()

	def set_crawl_done_info(self):
		cursor = self.conn.cursor()
		values = (self.jobid, int(self.node.id)-1)
		query = "INSERT INTO crawl_done(jobid, nodeid) VALUES "+str(values)
		cursor.execute(query);
		self.conn.commit()
		cursor.close()
				
	# crawl the input  
	def crawl(self, jobid, new_node=0):
		if int(jobid) == 0:
			return
		self.crawl_started = 1
		self.jobid = jobid
		node_id = int(self.node.id)-1
		lines = self.get_crawl_input(node_id, new_node)
		i=-1
		while i < (len(lines)) - 1:
			i+=1
			if len(self.new_nodes_list)>0:
				if self.new_node == -1:
					print("recalculating work")
					lines.extend(self.get_new_work())
					self.new_nodes_list =  []
					print("new work")
					print(lines)
					self.new_node = 0
				elif i == len(lines) - 1:
					print("recalculating work")
					print("skipped: " + lines[i])
					self.new_nodes_list = []
					self.new_node = 0
					continue
			url = lines[i].strip()
			c = Crawler([url], self.node.id)
			c.crawl()
			s_graph = sanitize(c.graph)
			self.save_crawl_result(s_graph, lines[i])
		self.set_crawl_done_info()
		print("crawling for node: "+ self.node.id + " done")
		if int(self.node.id) != PeerClient.master_node_id:
			self.crawl_started = 0
