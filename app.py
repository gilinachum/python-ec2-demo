import base64
import json

from flask import Flask, jsonify, abort, request
from datetime import datetime

app = Flask(__name__)


@app.route('/fetch')
def fetch():
    print(f'Starting')    
    return jsonify('{}')