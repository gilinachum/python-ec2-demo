import base64
import json
import urllib.request

from flask import Flask, jsonify, abort, request
from datetime import datetime
import boto3
import logging

logging.basicConfig(filename='/home/ec2-user/pythonapp.log',level=logging.DEBUG)

instanceId = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()
az = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/placement/availability-zone').read().decode()

logging.info(f'Starting. instanceId={instanceId}. az={az}')

app = Flask(__name__)

@app.route('/fetch')
def get():
    busy_wait_in_seconds  = request.args.get('busy_wait_in_seconds', default = 1, type = int)
    logging.info(f'Received request to wait {busy_wait_in_seconds} seconds.')
    
    record_metric(instanceId, busy_wait_in_seconds)
    busy_wait(busy_wait_in_seconds)
    
    return jsonify(instanceid=instanceId, availability_zone=az)
    
def busy_wait(dt):   
    import time
    current_time = time.time()
    while (time.time() < current_time+dt):
        pass
    
def record_metric(instance_id, busy_wait_in_seconds):
    client = boto3.client('cloudwatch')
    response = client.put_metric_data(
    Namespace='python-app',
    MetricData=[
        {
            'MetricName': 'calls',
            'Dimensions': [
                {
                    'Name': 'busy_wait_in_seconds',
                    'Value': str(busy_wait_in_seconds)
                },
                {
                    'Name': 'instance_id',
                    'Value': instance_id
                }
            ],
            'Value': 1,
            'Unit': 'None',
            'StorageResolution': 1
        },
    ])
    logging.info(f'recorded CW metric. Response={response}')
    return response