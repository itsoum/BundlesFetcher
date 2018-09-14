import json
import urllib.request
import re
import requests
import yaml
from collections import Counter
import itertools

import pandas as pd
import numpy as np

#DAG

#uDAG

with open('bundles_yaml/django-2.yml') as bundle:
	data = yaml.load(bundle)
	print(data['relations'])
	i=0
	relations = [r for r in data['relations']]
	print(relations[0][1])

	final = list(itertools.chain.from_iterable(relations))
	print(final)

	for f in final:
		#chname=f.rsplit(':',1)[-1]
		#print(chname)
		chname=f.rsplit(':',1)[0]
		print(chname)
		print(data['services'][chname]['charm'])


	am = pd.DataFrame(np.zeros(shape=(int(len(final)/2),int(len(final)/2))))
	print(am)	
	
	#relations
	#print(data['services'][relations]['charm'])


