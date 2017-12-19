import base64
import json
import urllib.request

from flask import Flask, jsonify, abort, request
from datetime import datetime

app = Flask(__name__)


@app.route('/fetch')
def get():
    instanceId = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()
    mac_id = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/network/interfaces/macs/').read().decode()
    subnet_id = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/network/interfaces/macs/' + mac_id +'/subnet-id/').read().decode()
    print(f'Starting')    
    return jsonify(instanceid=instanceId, subnet_id=subnet_id)