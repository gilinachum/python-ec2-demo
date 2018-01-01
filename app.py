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
    az = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/placement/availability-zone').read().decode()
    
    busy_wait(busy_wait_in_seconds)
    
    return jsonify(instanceid=instanceId, availability_zone=az)
    
def busy_wait(dt):   
    import time
    current_time = time.time()
    while (time.time() < current_time+dt):
        pass
    
def send_hit_metric():
    import boto3
    client = boto3.client('cloudwatch')
    