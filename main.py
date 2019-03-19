''' 
Imports
'''
from flask import Flask, request, make_response
from init_gh import GHFiles
import json, os, requests
import response
from github import Github

app = Flask(__name__)

def processRequest(reqType):
    req = request.get_json(silent=True, force=True)
    print("Data from application: ", req)
    func = getattr(response, ('makeResponseFor%s')%(reqType))
    res = func(req)
    res = json.dumps(res, indent=4)
    print("Response sent back: ", res)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/addUser', methods=['POST'])
def addUser():
    return processRequest('AddUser')

@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    return processRequest('CheckLogin')

@app.route('/whoAmI', methods=['POST'])
def whoAmI():
    return processRequest('WhoAmI')

@app.route('/schedule', methods=['POST'])
def schedule():
    return processRequest('Schedule')

@app.route('/authenticateNurse', methods=['POST'])
def authenticateNurse():
    return processRequest('AuthenticateNurse')

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
