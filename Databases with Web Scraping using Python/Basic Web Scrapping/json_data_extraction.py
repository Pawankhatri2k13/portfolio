import urllib.request, urllib.parse, urllib.error
import json

url = "http://py4e-data.dr-chuck.net/comments_519113.json"
data = urllib.request.urlopen(url).read()
info = json.loads(data)

info = info['comments']
print ('Retrieving', url, '\nRetrieved', len(data), 'caracters', '\nCount:', len(info))

num = 0
for item in info:
    num += int(item['count'])

print ('Sum:', num)