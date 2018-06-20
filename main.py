import json
import urllib.request


with urllib.request.urlopen("https://api.jujucharms.com/charmstore/v5/list?type=bundle") as url:
    data = json.loads(url.read().decode())
    j=0
    for i in data['Results']:
    	print(data['Results'][j]['Id'])
    	j+=1
    print(j)


