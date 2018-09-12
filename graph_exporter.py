import json
import urllib.request
import re
import requests
import yaml
from collections import Counter
import itertools


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

		
	
	#relations
	#print(data['services'][relations]['charm'])


