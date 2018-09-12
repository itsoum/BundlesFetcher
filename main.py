import json
import urllib.request
import re
import requests
import yaml
from collections import Counter


def charms_link_part(charm_name):
  return re.findall(r'[\w]*[^cs:]', charm_name)

def charms_list():
	with urllib.request.urlopen("https://api.jujucharms.com/charmstore/v5/list?type=charm") as url:
	    data = json.loads(url.read().decode())
	    j=0
	    charm_list=[]
	    for i in data['Results']:
	    	charm_name = ''.join(charms_link_part(data['Results'][j]['Id']))
	    	charm_list.append(charm_name)
	    	j+=1
	    return charm_list

def store_charmsmetad(charmsmetad):
	for charm in charmsmetad:
		print(charm)
		resp=urllib.request.urlopen('https://api.jujucharms.com/charmstore/v5/'+charm+'/archive/metadata.yaml')
		data = yaml.load(resp)
		chname=charm.rsplit('/',1)[-1] 
		with open('charms_metadata_yaml/'+chname+'.yml', 'w') as yaml_file:
		    yaml.dump(data, yaml_file, default_flow_style=False)
	return

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

def store_bundles(bundles):
	for bundle in bundles:
		print(bundle)
		resp=urllib.request.urlopen('https://api.jujucharms.com/charmstore/v5/' + bundle + '/archive/bundle.yaml')
		data = yaml.load(resp)
		buname=bundle.split("bundle/",1)[1] 
		with open('bundles_yaml/'+buname+'.yml', 'w') as yaml_file:
		    yaml.dump(data, yaml_file, default_flow_style=False)
	return

#---------------------------
def unique_charms(charms_list):
	j=0
	unique_charms_list=[]
	for charm in charms_list:
		chname=charm.rsplit('/',1)[-1]
		print(chname)
		chname=chname.rsplit('-',1)[0]
		print(chname)
		unique_charms_list.append(chname)
		j+=1
	return unique_charms_list


charms=charms_list()
nbld=unique_charms(charms)
duplicates=Counter(nbld)
print(duplicates)
#print(nbld)

#Connection failed in the meantime
#l = [charms.index(i) for i in charms if '~landscape/trusty/neutron-api-leadership-election-0' in i]
#k=l[0]
#print(k)
#charms=charms[k:]
#print(charms)

#store_charmsmetad(charms)

#bundles=bundles_list()
#store_bundles(bundles)

