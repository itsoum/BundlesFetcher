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

#-----------------------------------------------------------------------
# CSV files
#  - links for the direct relations per graph (adjacent matrix)
#  - gdistances for the Djikstra shortest paths
#    between all nodes per graph (distances matrix)
#-----------------------------------------------------------------------
outfile_links = "links.csv"
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
# JUJU Dataset formation
# considering each bundle as uDAG (undirected graph)
#-----------------------------------------------------------------------

j=0
k=0
k1=[]
# directory of descriptors
path = "bundles_yaml/"
# list of bundles
filelist = os.listdir(path)
for i in filelist:
	print(path+i)
	j+=1
	print(j)
	with open(path+i) as bundle:
		
		data = yaml.load(bundle)
		try:
			relations = [r for r in data['relations']]
			final = list(itertools.chain.from_iterable(relations))
			print(final)
			listcharmfullname=[]
			flag=1
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

				if(flag%2==0):
					
					if(tempfinalcharm == finalcharm):
						tempfinalcharm=tempfinalcharm+'/'+tempchservicename
						finalcharm=finalcharm+'/'+chname
					# Write new row on links.csv
					row = [ i, tempfinalcharm, finalcharm]
					csvwriter_links.writerow(row)
				else:
					tempfinalcharm=finalcharm
					tempchservicename=chname
				flag+=1
		except:
			k1.append(path+i)

			k+=1
print('ta leme',k,k1)



