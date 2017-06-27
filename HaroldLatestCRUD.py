#!flask/bin/python


from flask import Flask, jsonify, request, abort, make_response
from flask_httpauth import HTTPBasicAuth
import requests

auth = HTTPBasicAuth()
app = Flask(__name__)

@auth.get_password
def get_password(username):
	if username == 'sti':
		return 'sti'
	return None
######################### error handler ##################
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'Error': 'Unauthorized access'}), 401)
@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error':'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'Error 4O4':'Not found'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
	return make_response(jsonify({'Error 405':'Method not allowed'}), 405)

@app.errorhandler(409)
def duplicatefound(error):
        return make_response(jsonify({'error':'DUplicate item found'}), 405)


##################### LOGIN, SESSIONS,ETC ##########################
@app.route('/rackhd/login', methods=['POST'])
@auth.login_required
def rackhd_login():
	#if not request.json or not 'username' in request.json:
	#	abort(400)

	user =  request.json['username']
	pw = request.json['password']
	
	url = "https://localhost:8443/login"
	payload = '{"username" : "' + user + '", "password" : "' + pw +'"}'
	headers= {"Content-Type": "application/json"}
	r = requests.post(url, headers=headers, data=payload, verify=False)
	return r.text

@app.route('/redfish/login',methods=['POST'])
@auth.login_required
def redfish_login():
	user =  request.json['username']
        pw = request.json['password']

        url = "https://localhost:8443/redfish/v1/SessionService/Sessions"
        payload = '{"UserName" : "' + user + '", "Password" : "' + pw +'"}'
        headers= {"Content-Type": "application/json"}
        r = requests.post(url, headers=headers, data=payload, verify=False)
        return r.text

@app.route('/redfish/readsessions', methods=['GET'])
@auth.login_required
def redfish_session():
	url = "https://localhost:8443/redfish/v1/SessionService/Sessions/"
	headers = {"content-type":"application/json"}
	
	r = requests.get(url, headers=headers, auth=('admin','admin123'), verify=False)
	return r.text

@app.route('/redfish/deletesessions', methods=['DELETE'])
@auth.login_required
def redfish_delsession():
	sid = request.args.get('id')
	url = "https://localhost:8443/redfish/v1/SessionService/Sessions/%s" % sid
	r = requests.delete(url, auth=('admin','admin123'), verify=False)
	return r.text


  #######################################################################
				#NODES
   #####################################################################


	
@app.route('/rackhd/nodes', methods=['GET'])
@auth.login_required
def readnode():
	token = request.headers.get('token')
	url = "https://localhost:8443/api/current/nodes"
	headers = {"Content-Type":"application/json", "Authorization":"JWT "+token
	}
	r = requests.get(url, headers=headers, verify=False)

	return r.text

@app.route('/rackhd/nodes', methods=['POST'])
@auth.login_required
def createnode():

	name = request.json['name']
	typ = request.json['typ']
	token = request.headers.get('token')
	url = "https://localhost:8443/api/current/nodes"

	payload = '{"name":"%s","type":"%s","autoDiscover":false}' % (name,typ)

	headers= {"Content-Type": "application/json", "Authorization": "JWT "+token}

	r = requests.post(url, headers=headers, data=payload, verify=False)
	return payload

##### *****NOTE: ONCE DELETED AN ERROR 400 WILL BE PRODUCED, BUT THE NODE IS ACTUALLY DELETED SUCCESSFULLY, ITS A BUG #############
@app.route('/rackhd/nodes', methods=['DELETE'])
@auth.login_required
def deletenode():
	ids = request.args.get('ids')
	token = request.headers.get('token')
	url = "https://localhost:8443/api/current/nodes/%s" % ids
	headers= {"Content-Type":"application/json",
"Authorization":"JWT "+token}

	r = requests.delete(url, headers=headers, verify=False)
	return r.text
	
@app.route('/rackhd/nodes',methods=['PATCH'])
@auth.login_required
def updatenode():
	token = request.headers.get('token')
	ids = request.args.get('ids')
	field = request.json['field']
	data = request.json['data']
	
	url = "https://localhost:8443/api/current/nodes/%s" % ids
	payload = '{"%s": "%s"}' %(field,data)
	headers= {"Content-Type":"application/json",
"Authorization":"JWT "+token}
	r = requests.patch(url, headers=headers, data=payload, verify=False)
	return r.text


	#############################     TAGS   ########################################  

@app.route('/rackhd/tags/create',methods=['POST'])
@auth.login_required
def createtag():
        token = request.headers.get('token')
        name = request.json['name']
        cpath = request.json['cpath']
        contains = request.json['contains']
	epath = request.json['epath']
	equals = request.json['equals']

        url = "https://localhost:8443/api/current/tags"
        payload = '{"name":"%s", "rules": [{"path":"%s", "contains":"%s"}, {"path":"%s", "equals":"%s"}]}'% (name,cpath,contains,epath,equals)

        headers= {"Content-Type":"application/json",
"Authorization":"JWT "+token}
        r = requests.post(url, headers=headers, data=payload, verify=False)
        return r.text

@app.route('/rackhd/tags/read', methods=['GET'])
@auth.login_required
def readtag():
	token = request.headers.get('token')
	url = "https://localhost:8443/api/current/tags/"
	headers= {"Content-Type":"application/json", "Authorization":"JWT "+token}	
	r = requests.get(url, headers=headers, verify=False)
	return r.text

@app.route('/rackhd/tags/update', methods=['PATCH'])
#**add tags to NODE**
@auth.login_required
def updatetag():
	token = request.headers.get('token')
	node_id = request.args.get('id')
	tags = request.json['tags']
	url = "https://localhost:8443/api/current/nodes/%s/tags" % node_id
	
	headers= {"Content-Type":"application/json", "Authorization":"JWT "+token}
	payload = '{"tags":["%s"]}' % tags

	r = requests.patch(url, headers=headers, data=payload, verify=False)
	return r.text

@app.route('/rackhd/tags/delete', methods=['DELETE'])
@auth.login_required
def deletetag():
	token = request.headers.get('token')
	tag_name = request.args.get('name')
	url = "https://localhost:8443/api/current/tags/%s" % tag_name
	headers = {"content-type":"application/json", "Authorization":"JWT "+token}
	r = requests.delete(url, headers=headers, verify=False)
	return r.text

@app.route('/rackhd/nodes/readtag', methods=['GET'])
@auth.login_required
def readnodetag():
	token = request.headers.get('token')
	node_id = request.args.get('nodeid')
	url = "https://localhost:8443/api/current/nodes/%s/tags" % node_id
	headers = {"content-type":"application/json", "Authorization":"JWT "+token}

	r = requests.get(url, headers=headers, verify=False)
	return r.text

@app.route('/rackhd/nodes/deletetag', methods=['DELETE'])
@auth.login_required
def deletetagfromnode():
	token = request.headers.get('token')
	node_id = request.args.get('nodeid')
	tag_name = request.args.get('tagname')
	
	url = "https://localhost:8443/api/current/nodes/%s/tags/%s" % (node_id,tag_name)
	headers = {"content-type":"application/json", "Authorization":"JWT "+token}
	r = requests.delete(url, headers=headers, verify=False)
	return r.text

     #############################   HOOOK ###############################

@app.route('/rackhd/hook', methods=['POST'])
@auth.login_required
def createhook():
	token = request.headers.get('token')
	link = request.json['url']
	url = "https://localhost:8443/api/2.0/hooks"
	payload = '{"url":"%s"}' % link
	headers = {"content-type":"application/json","Authorization":"JWT " +token}
	
	r = requests.post(url, headers=headers, data=payload, verify=False)
	return r.text

@app.route('/rackhd/hook', methods=['GET'])
@auth.login_required
def readhook():
	token = request.headers.get('token')
	url = "https://localhost:8443/api/2.0/hooks"
	headers = {"content-type":"application/json", "Authorization":"JWT "+ token}
	r = requests.get(url, headers=headers, verify=False)
	return r.text

@app.route('/rackhd/hook', methods=['PATCH'])
@auth.login_required
def updatehook():
	token = request.headers.get('token')
	hook_id = request.args.get('hook_id')
	field = request.json['field']
	data = request.json['data']
	#name = request.json['name']
	url = "https://localhost:8443/api/2.0/hooks/%s" % hook_id
	
	payload = '{"%s":"%s"}' % (field,data)
	headers = {"content-type":"application/json", "Authorization": "JWT "+token}
	
	r = requests.patch(url, headers=headers, data=payload, verify=False)
	return r.text

@app.route('/rackhd/hook', methods=['DELETE'])
@auth.login_required
def deletehook():
	token = request.headers.get('token')
	hook_id = request.args.get('hook_id')
	url = "https://localhost:8443/api/2.0/hooks/%s" % hook_id
	headers = {"content-type":"application/json", "Authorization":"JWT "+token}
	
	r = requests.delete(url, headers=headers, verify=False)
	return r.text



if __name__ == '__main__':
	app.run(debug=True)
