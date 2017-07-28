import requests
import sys
import pprint

r = requests.get('http://localhost:8069/search', json={'query': ' '.join(sys.argv[1:])})
print(r)

pprint.pprint(r.json())

