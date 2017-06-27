#  HAROLD'S README FOR REDFISH FLASK

   CRUDs: NODES, TAGS, HOOKS
   HTTPAuth credentials: sti:sti
   Redfish admin credentials: admin:admin123

## GETTING STARTED
	Run the program using ./<filename>.py

###  NOTE: "content-type: application/json" must be included in header whenever sending json data. 
       Pipe output to python -m json.tool to view the data in a better format. (e.g. curl xxxxxx.com | python -m json.tool)

#### CRUDs
---------------------------------
	     LOGIN
---------------------------------
Description:
Login to obtain auth_token to carry out CRUD operation on rackhd/redfish

Operation: POST

Path: /rackhd/login

Parameters:
"username","password" -  username and password of an account to authenticate with, enter in json format.

Curl command example:
curl -X POST "http://localhost:5000/rackhd/login" -H  "content-type: application/json" -d '{ "username": "admin",  "password": "admin123"}' -u sti:sti


----------------------------------
	  CREATE NODES
----------------------------------
Description:
Create a new node

Operation: POST

Path: /rackhd/nodes

Parameters:
"token" - auth_token, enter in the header.
"name","typ" - name and type of the switch respectively, enter in json format.

Curl command:
curl -X POST "http://localhost:5000/rackhd/nodes" -H  "token: <Enter auth_token here>" -H  "content-type: application/json" -d '{ "name": "<Enter name here>",  "typ": "<Enter type here>"}'


----------------------------------
	    READ NODES
----------------------------------
Description:
Get a list of all the nodes

Operation: GET

Path: /rackhd/nodes

Parameters:
"token" - auth_token, enter in header

Curl command:
curl -X GET "http://localhost:5000/rackhd/nodes" -H  "token: <enter auth_token here>" -u sti:sti | python -m json.tool


----------------------------------
	    UPDATE NODES
----------------------------------
Description:
Update a data of a specific node

Operation: PATCH

Path: /rackhd/nodes

Parameters:
"token" - auth_token, enter in header
"ids" - ID of the node to update, URL Query String
"field" - Specific field to update(e.g. type/autoDiscover), enter as json data
"data" - New data to update the field with, enter as json data.

Curl command:
curl -X PATCH "http://localhost:5000/rackhd/nodes?ids=<Enter node ID here>" -H  "token: <enter auth_token here>" -H "content-type:application/json" -d '{"field":"<enter field to update>","data":"<enter data>"}' -u sti:sti


----------------------------------
	    DELETE NODES
----------------------------------
Description:
Delete a specific node

Operation: DELETE

Path: /rackhd/nodes

Parameters:
"token" - auth_token, enter in header
"ids" - ID of the node to delete, URL Query String

***NOTE***: WHEN CURL DELETE COMMAND IS RUN AN ERROR 400 WILL BE PRODUCED, BUT THE NODE IS ACTUALLY DELETED SUCCESSFULLY, ITS A BUG 

Curl command:
curl -X DELETE "http://localhost:5000/rackhd/nodes?ids=<Enter node ID>" -H  "token: <Enter auth_token here>" -u sti:sti


----------------------------------
	  CREATE TAGS
----------------------------------
Description:
Create a new tag

Operation: POST

Path: /rackhd/tags/create

Parameters:
"token" - auth_token, enter in the header.
"name" - name of the new tag, enter in json format.
"cpath" - Path into the catalog to validate against. For "contains", json data.
"contains" - A string that the value should contain, json data.
"epath" - Path into the catalog to validate against. For "equals", json data.
"equals" - Exact value to match against. Json data.

Curl command with sample data:
curl -X POST "http://localhost:5000/rackhd/tags/create" -u sti:sti -H  "token: <enter auth_token here>" -H  "content-type: application/json" -d '{  "name": "AMD 32GB RAM",  "cpath": "dmi.Base Board Information.Manufacturer",  "contains": "Intel",  "epath": "dmi.memory.total",  "equals": "329483092KB"}"'


----------------------------------
	  READ TAGS
----------------------------------
Description:
Get a list of tags

Operation: GET

Path: /rackhd/tags/read

Parameters:
"token" - auth_token, enter in the header.

Curl command:
curl -X GET "http://localhost:5000/rackhd/tags/read" -H  "token: <Enter auth_token here>" -u sti:sti


----------------------------------
	  UPDATE TAGS
----------------------------------
Description:
Add the TAG onto a node by patching the /tags path of a node

Operation: PATCH

Path: /rackhd/tags/update

Parameters:
"token" - auth_token, enter in the header.
"id" - ID of the node to update, URL Query string
"tags" - name of tags to add, json data

Curl command:
curl -X PATCH "http://localhost:5000/rackhd/tags/update?id=<Enter Node ID here>" -H  "token: <Enter auth_token here>" -H "content-type:application/json" -d '{"tags":"<Enter tags here>"}' -u sti:sti

----------------------------------
	  DELETE TAGS
----------------------------------
Description:
Delete a specific tag

Operation: DELETE

Path: /rackhd/tags/update

Parameters:
"token" - auth_token, enter in the header.
"name" - name of tags to delete, URL query string

Curl command:
curl -X DELETE "http://localhost:5000/rackhd/tags/delete?name=<Enter tag name here>" -H  "token: <Enter auth_token here>" -u sti:sti


----------------------------------
	READ TAGS OF A NODE
----------------------------------
Description:
Get a list of tags assigned to a specific node

Operation: GET

Path: /rackhd/nodes/readtag

Parameters:
"token" - auth_token, enter in the header.
"nodeid" - ID of the node to read, URL query string

Curl command:
curl -X GET "http://localhost:5000/rackhd/nodes/readtag?nodeid=<Enter node ID here>" -H  "token: <Enter auth_token here>" -u sti:sti


----------------------------------
     DELETE TAGS FROM A NODE
----------------------------------
Description:
Delete a specific tag from a specific node

Operation: DELETE

Path: /rackhd/nodes/deletetag

Parameters:
"token" - auth_token, enter in the header.
"nodeid" - ID of the node to delete the tag from, URL query string
"tagname" - name of tags to delete, URL query string

Curl command:
curl -X DELETE "http://localhost:5000/rackhd/nodes/deletetag?nodeid=<Enter Node ID here>&tagname=<Enter tag name here>" -H  "token: <Enter auth_token here>" -u sti:sti


----------------------------------
	 CREATE HOOKS
----------------------------------
Description:
Create a new hook

Operation: POST

Path: /rackhd/hook

Parameters:
"token" - auth_token, enter in the header.
"url" - url of the new hook, json data

Curl command:
curl -X POST "http://localhost:5000/rackhd/hook" -H  "token: <Enter auth_token here>" -H  "content-type: application/json" -d '{ "url": "<enter URL here>"}' -u sti:sti


----------------------------------
	 READ HOOKS
----------------------------------
Description:
Get the list of hooks

Operation: GET

Path: /rackhd/hook

Parameters:
"token" - auth_token, enter in the header.

Curl command:
curl -X GET "http://localhost:5000/rackhd/hook" -H  "token: <Enter token here>" -u sti:sti


----------------------------------
	UPDATE HOOKS
----------------------------------
Description:
Update data of hooks

Operation: PATCH

Path: /rackhd/hook

Parameters:
"token" - auth_token, enter in the header.
"hook_id" - ID of the hook to be updated, URL query string
"field" - Field to update, json data
"data" -  data to update, json data

Curl command:
curl -X PATCH "http://localhost:5000/rackhd/hook?hook_id=<Enter Hook ID here>" -H  "token: <Enter token here>" -H "content-type:application/json" -d '{"field":"<enter field to update>","data":"<enter data to update>"}' -u sti:sti


----------------------------------
	DELETE HOOKS
----------------------------------
Description:
Delete a specific hook

Operation: DELETE

Path: /rackhd/hook

Parameters:
"token" - auth_token, enter in the header.
"hook_id" - ID of the hook to be deleted, URL query string

Curl command:
curl -X DELETE "http://localhost:5000/rackhd/hook?hook_id=<Enter Hook ID here>" -H  "token: <Enter token here>" -u sti:sti
