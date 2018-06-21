import json
import urllib.request
import re

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
	    	#print(bundle_name)
	    	j+=1
	    #print(bundle_list)
	    #print(j)
	    return bundle_list

 https://api.jujucharms.com/charmstore/v5/bundle/<bundle-name>/archive/bundle.yaml

with urllib.request.urlopen("https://api.jujucharms.com/charmstore/v5/list?type=bundle") as url:
	    data = json.loads(url.read().decode())
	    j=0
	    bundle_list=[]
	    for i in data['Results']:
	    	bundle_name = ''.join(bundles_link_part(data['Results'][j]['Id']))
	    	bundle_list.append(bundle_name)
	    	#print(bundle_name)
	    	j+=1
	    #print(bundle_list)
	    #print(j)
	    return bundle_list



