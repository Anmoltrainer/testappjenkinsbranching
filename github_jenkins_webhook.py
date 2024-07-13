from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

JENKINS_URL = os.environ.get('JENKINS_URL')
JENKINS_JOB = os.environ.get('JENKINS_JOB')
JENKINS_USER = os.environ.get('JENKINS_USER')
JENKINS_API_TOKEN = os.environ.get('JENKINS_API_TOKEN')

@app.route('/github-webhook/', methods=['POST'])
def github_webhook():
    if request.method == 'POST':
        payload = request.json
        if payload['ref'] == 'refs/heads/main':
            trigger_jenkins_build()
            return jsonify({'message': 'Jenkins build triggered'}), 200
    return jsonify({'message': 'Webhook received'}), 200

def trigger_jenkins_build():
    url = f"{JENKINS_URL}/job/{JENKINS_JOB}/build"
    auth = (JENKINS_USER, JENKINS_API_TOKEN)
    
    response = requests.post(url, auth=auth)
    
    if response.status_code == 201:
        print("Jenkins build triggered successfully")
    else:
        print(f"Failed to trigger Jenkins build. Status code: {response.status_code}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
