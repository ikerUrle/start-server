from flask import Flask, jsonify, render_template
from waitress import serve
import logging
import requests
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NODE = 'y'

try:
    AUTH = os.environ['PVE_TOKEN']
    SERVER = os.environ['PVE_SERVER']
except:
    print("Env variables missing")
    exit()

def call_api(endpoint,method = 'GET'):
    base_url = f'https://{SERVER}/api2/json'
    url = base_url + endpoint
    headers = {
        'Authorization' : AUTH
    }
    if (method == 'POST'):
        r = requests.post(url,headers=headers)
    else:
        r = requests.get(url,headers=headers)
    if (r.status_code != 200) :
        response = {
            "status": "error",
            "message": r.text 
        }
        logger.error(f"Command execution failed: {r.text}")
    else:
        response = {
            "status": "success",
            "output": r.json() 
        }
        logger.info(f"Command executed successfully: {r.json()}")
    return jsonify(response)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_vm():
    return call_api(f"/nodes/{NODE}/qemu/104/status/start","POST")

@app.route('/status', methods=['GET'])
def status_vm():
    return call_api(f"/nodes/{NODE}/qemu/104/status/current")

if __name__ == '__main__':
    # call_api()
    serve(app,host='0.0.0.0',port=5000)
