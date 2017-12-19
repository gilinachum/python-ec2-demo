import base64
import json
import urllib.request

from flask import Flask, jsonify, abort, request
from datetime import datetime

app = Flask(__name__)
    
@app.route('/fetch')
def get():
    busy_wait_in_seconds  = request.args.get('busy_wait_in_seconds', default = 1, type = int)
    
    print(f'Starting') 
    instanceId = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()
    mac_id = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/network/interfaces/macs/').read().decode()
    subnet_id = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/network/interfaces/macs/' + mac_id +'/subnet-id/').read().decode()
    
    busy_wait(busy_wait_in_seconds)
    
    return jsonify(instanceid=instanceId, subnet_id=subnet_id)
    
def busy_wait(dt):   
    import time
    current_time = time.time()
    while (time.time() < current_time+dt):
        pass