# create a flask server
# server will accept some input 
# server will then print something 
# server will then sleep for a bit (simulate processing)
# server will print something again 
# server will be ready to accept the next request 
# maybe print something is actually sending the request somewhere else? 

from flask import Flask, jsonify, request, abort
import time

app = Flask(__name__)

# Define route to handle requests to the root URL ('/')
@app.route('/')
def index():
    return "Welcome to Flask REST API Demo! "

# Health check route (GET)
# This endpoint returns a 200 OK status and a JSON response to confirm that the service is running.
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200  # Return HTTP status 200 OK

# Send process request 
@app.route('/test',methods=['GET'])
def test_check():
    
    total = 0
    for i in range(10**8):
        total += i
    
    return jsonify({"status":"Test completed"}),201

# Entry point for running the Flask app
# The app will run on host 0.0.0.0 (accessible on all network interfaces) and port 8000.
# Debug mode is disabled (set to False).
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)