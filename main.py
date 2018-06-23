import json
import urllib.request
import re
import requests
import yaml

def bundles_link_part(bundle_name):
  return re.findall(r'[\w]*[^cs:]', bundle_name)

def bundles_list():
	with urllib.request.urlopen("https://api.jujucharms.com/charmstore/v5/list?type=bundle") as url:
	    data = json.loads(url.read().decode())
	    j=0
	    bundle_list=[]
	    for i in data['Results']:
	    	bundle_name = ''.join(bundles_link_part(data['Results'][j]['Id']))
	    	bundle_list.append(bundle_name)
	    	j+=1
	    return bundle_list

bundles=bundles_list()

for bundle in bundles:
	print(bundle)
	resp=urllib.request.urlopen('https://api.jujucharms.com/charmstore/v5/' + bundle + '/archive/bundle.yaml')
	data = yaml.load(resp)
	buname=bundle.split("bundle/",1)[1] 
	with open('bundles_yaml/'+buname+'.yml', 'w') as yaml_file:
	    yaml.dump(data, yaml_file, default_flow_style=False)



