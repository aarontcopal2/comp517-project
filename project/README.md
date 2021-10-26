# Comp517 Project Hacking

You will identify and contribute to the understanding and
knowledge on a problem related to operating systems. It is
anticipated that this project will identify a compelling and
technically interesting problem and make concrete progress
towards solving that problem. The project must emphasize
original contributions to the conversation on the topic and
result in a real software artifacts as well as evidence to
support the hypothesis for how to solve the problem. You
will sketch out the problem, related literature, and plan in
the [project proposal](../proposal/README.md) and execute
its plan with code located in this directory. 

The primary objective of this project is to make a
hypothesis for addressing a current problem. A project will
typically take one of two forms: 1) system that includes
novel design and implementation elements to address the gap
in the literature or 2) devises a hypothesis and explores a
concrete phenomena of interest in an empirical
investigation. 

## Grading

Grading projects is hard to define in general, however, it
is anticipated that you will produce code that I can run and
test out. That you will generate artifacts demonstrating
that your idea does in fact address the problem you propose
and is distinct from related work. It need not be successful
in producing better results, but we should learn something
from the investigation. It is anticipated that at the
[midterm report](../midterm/README.md) you will a running
prototype that you can demo. For the final we anticipate an
independent project that can be run by the professor.


## How to run it
1. Move to the main directory
`cd peer-discovery`

2. Create a folder for saving ouptut files
`mkdir output`

2. Start a master peer using the script
`python master_peer.py`

3. Start a peer using the script peer.py. Pass the ip_address:port and node id. Eg: 
`python peer.py 127.0.0.1:8001 2`

    (The peer you just started will connect with master peer and exchange messages)

4. After master and peer nodes establish connection, you can start to send crawl requests to master peer. Type in
`input.txt`
    to the master peer to send a crawl request. You should already have list of urls in the input.txt file and the master peer will send this info to all connected peers.
* Watch the magic happen. Make sure you have the output/ directory checked out. 
* You will find the `crawl_output.json` file inside the output directory which will have the combined results of crawling from all peers. 
* After the crawling is done, the master peer will then shoot a request for pagerank and will combine them in the same directory with the file `pagerank_output` 
