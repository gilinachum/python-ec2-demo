import urllib.request

def busy_wait(dt):   
    import time
    current_time = time.time()
    while (time.time() < current_time+dt):
        pass
        


instanceid = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()
mac_id = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/network/interfaces/macs/').read().decode()
subnet_id = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/network/interfaces/macs/' + mac_id +'/subnet-id/').read().decode()
az_id = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/placement/availability-zone').read().decode()
#busy_wait(0)


print(az_id)