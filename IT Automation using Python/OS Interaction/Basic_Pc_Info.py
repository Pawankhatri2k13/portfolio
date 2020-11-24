import shutil
import psutil
import socket
import requests

###
def check_disk_usage(disk):
    du = shutil.disk_usage(disk)
    free = du.free/du.total*100
    return free>20
print(check_disk_usage("/"))

###
def check_cpu_usage():
    usage = psutil.cpu_percent(1)
    return usage < 75
print(check_cpu_usage())


###
localhost = socket.gethostbyname('localhost')
print(localhost)


###
request = requests.get("http://www.google.com")
print(request.status_code)

