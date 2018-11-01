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


#-----------------------------------------------------------------------
# CSV files
#  - links for the direct relations per graph (adjacent matrix)
#  - gdistances for the Djikstra shortest paths
#    between all nodes per graph (distances matrix)
#-----------------------------------------------------------------------
outfile_links = "links_raw.csv"
outfile_gdist = "gdistances.csv"

#-----------------------------------------------------------------------
# open two files to write (mode "w"), and create two CSV writer objects
#-----------------------------------------------------------------------
csvfile_links = open(outfile_links, "w")
csvwriter_links = csv.writer(csvfile_links)

csvfile_gdist = open(outfile_gdist, "w")
csvwriter_gdist = csv.writer(csvfile_gdist)

#-----------------------------------------------------------------------
# add headings to CSV files
#-----------------------------------------------------------------------
row = [ "graph", "component", "component" ]
csvwriter_links.writerow(row)
row = [ "graph", "component", "component", "distance" ]
csvwriter_gdist.writerow(row)


#-----------------------------------------------------------------------
# Remove duplicates from csv
#-----------------------------------------------------------------------
def duplicates(read,write):
	with open(read,'r') as in_file, open(write,'w') as out_file:
	    # Set for fast O(1) amortized lookup
	    seen = set() 
	    for line in in_file:
	    	# Skip duplicate
	        if line in seen: continue
	        seen.add(line)
	        out_file.write(line)
	return 0

#-----------------------------------------------------------------------
# Create a graph and calculate the graph distances
#-----------------------------------------------------------------------
def gdistances(listcharmfullname):
	
	# initialize a graph
	G=nx.Graph()	
	#remove duplicates from the list
	l=list(set(listcharmfullname))
	# add nodes
	G.add_nodes_from(l)	
	# add graph edges
	for n in range(len(listcharmfullname)):
		if(n>0 and n%2 !=0 ):
			#print(listcharmfullname[n-1], listcharmfullname[n])
			G.add_edge(listcharmfullname[n-1], listcharmfullname[n])
	# print(G.nodes())
	# print(G.edges())

	# find shortest path for all the component-pairs
	gd = nx.all_pairs_shortest_path_length(G)
	#for value in gd:
		#print(value)
	return gd

#-----------------------------------------------------------------------
# Main Flow 
# JUJU Dataset formation
# considering each bundle as uDAG (undirected graph)
#-----------------------------------------------------------------------

files_counter=0
exceptions_counter=0
ignored_bundles=[]

# directory of descriptors
path = "bundles_yaml/"

# list of bundles
filelist = os.listdir(path)

for i in filelist:
	files_counter+=1
	#print(files_counter)
	
	with open(path+i) as bundle:
		
		data = yaml.load(bundle)
		try:
			relations = [r for r in data['relations']]
			final = list(itertools.chain.from_iterable(relations))
			
			listcharmfullname=[]
			flag=1
			
			for f in final:

				# Service of charm
				chname=f.rsplit(':',1)[0]

				# Endpoint of charm
				#chservicename=f.rsplit(':',1)[1]
				
				try:
					charmfullname=data['services'][chname]['charm']
				except:
					charmfullname=data['applications'][chname]['charm']
				#listcharmfullname.append(charmfullname.rsplit('-',1)[0]) 

				# Charm full name
				finalcharm=charmfullname.rsplit('-',1)[0]


				#-----------------------------------------------------------------------
				# The same charm used in the relation but with different service of it,
				# then we characterize the charm with this expand '/service_name'
				#-----------------------------------------------------------------------
				if(flag%2==0):
					if(tempfinalcharm == finalcharm):
						tempfinalcharm=tempfinalcharm+'/'+tempchservicename
						finalcharm=finalcharm+'/'+chname
						temp2=len(listcharmfullname)
						listcharmfullname[temp2-1]=tempfinalcharm
						tempfinalcharm='temp'
					
					# Create the list of charms(with full name) per bundle
					# keeping the relatiions(for that there are duplicates)
					listcharmfullname.append(finalcharm)

					#-----------------------------------------------------------------------
					# Write new row on links_raw.csv
					#-----------------------------------------------------------------------
					row = [ i, tempfinalcharm, finalcharm]
					csvwriter_links.writerow(row)

				else:
					tempfinalcharm=finalcharm
					tempchservicename=chname
					listcharmfullname.append(finalcharm)
				
				flag+=1
		except:
			ignored_bundles.append(path+i)

			exceptions_counter+=1
		
		gd=gdistances(listcharmfullname)
		for value in gd:
			#print(value)		
			for key, value2 in value[1].items():
				#print(key,value2)
				row = [ i, value[0], key, value2 ]
				csvwriter_gdist.writerow(row)

print('In the exception case',exceptions_counter,ignored_bundles)

duplicates('links_raw.csv','links.csv')

