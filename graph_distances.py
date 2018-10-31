import json
import urllib.request
import re
import requests
import yaml
import itertools
import pandas as pd
import numpy as np
import csv
import os
from collections import Counter

import networkx as nx

G=nx.Graph()
'''
# adding just one node:
G.add_node("a")
# a list of nodes:
G.add_nodes_from(["b","c"])

print("Nodes of graph: ")
print(G.nodes())
print("Edges of graph: ")
print(G.edges())

'''

#-----------------------------------------------------------------------
# JUJU Dataset formation
# considering each bundle as uDAG (undirected graph)
#-----------------------------------------------------------------------
j=0
k=0
k1=[]
# directory of descriptors
path = "bundles_yaml/oai-5g-cran-slice-1.yml"
# list of bundles
#filelist = os.listdir(path)
print(path)
j+=1
print(j)
with open(path) as bundle:
	
	data = yaml.load(bundle)

	relations = [r for r in data['relations']]
	final = list(itertools.chain.from_iterable(relations))
	print(final)
	print(relations)
	listcharmfullname=[]
		
	for f in final:
		# Service of charm
		chname=f.rsplit(':',1)[0]
		print(chname)

		# Endpoint of charm
		'''
		chservicename=f.rsplit(':',1)[1]
		print(chservicename)
		'''

		try:
			charmfullname=data['services'][chname]['charm']
		except:
			charmfullname=data['applications'][chname]['charm']

		listcharmfullname.append(charmfullname.rsplit('-',1)[0]) 
		
		# Charm full name
		finalcharm=charmfullname.rsplit('-',1)[0]
		print(finalcharm)
	print('+++++++++++++++++++++++++')	
	#G.add_edges_from(relations)
	#remove duplicates
	l=list(set(listcharmfullname))
	print(l)
	print(listcharmfullname)
	G.add_nodes_from(l)
		

	for n in range(len(listcharmfullname)):
		if(n>0 and n%2 !=0 ):
			print(listcharmfullname[n-1], listcharmfullname[n])
			G.add_edge(listcharmfullname[n-1], listcharmfullname[n])
		#print(listcharmfullname[n])
	print('-----------------------------')	
	print(G.nodes())
	print(G.edges())

	print('-----------------------------')
	sp = nx.all_pairs_shortest_path_length(G)
	node1='cs:~navid-nikaein/xenial/oai-rru'
	node2='cs:~navid-nikaein/xenial/oai-spgw'
	print(sp)
	for value in sp:
		print(value)
	#for node1 in sp:
		#for node2 in sp[node1]:
			#print("Length between", node1, "and", node2, "is", sp[node1][node2])

