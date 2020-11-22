
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl


#Scraping HTML Data

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html = urlopen('http://py4e-data.dr-chuck.net/comments_519110.html', context=ctx).read()
soup = BeautifulSoup(html, "html.parser")
tags = soup('span')

summation = 0
count = 0
for tag in tags:
    count += 1    
    summation += int(tag.contents[0])
print('Count', count, '\nSum', summation)


#Following HTML Links
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "http://py4e-data.dr-chuck.net/known_by_Leni.html"
num = 7
pos = 18
print('Retrieving: ', url)

for times in range(int(num)):
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    print('Retrieving: ', tags[int(pos)-1].get('href', None))
    url = tags[int(pos)-1].get('href', None)