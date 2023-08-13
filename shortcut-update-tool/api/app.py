import io
import mimetypes
import os
import json
from datetime import datetime


from flask import (Flask, flash, redirect, render_template, request, send_file,
                   session, url_for, Response)
from flask_cors import CORS 
from HTTPResponses import *

# initialize app flask object
# intializing to the name of the file
app = Flask(__name__)
# https://stackoverflow.com/questions/20035101/why-does-my-javascript-code-receive-a-no-access-control-allow-origin-header-i
CORS(app)

REPO = r'C:\Users\omnic\local\GitRepos\apple-shortcuts'

# ----------------------------------------------------------------------------------------------------
# for the root of the website, we would just pass in "/" for the url
@app.route('/')
def index():
    # render index html which contains the form
    # form submission will route to /submitForm
    return 'Hello World'

@app.route('/get-updates-file', methods=['POST', 'GET'])
def get_updates_file():
    # Expecting the following keys
    # summary options and chat package
    # request.json should be in format of apiutils/samples/sample_api_request_1.json
    if request.json is None:
        return error_response(400, message='No JSON content included!')
    
    if 'path' not in request.json:
        return error_response(400, message='Missing keys!')
    
    path = request.json['path']
    if not os.path.exists(request.json['path']):
        return error_response(400, message=f'The specified path "{path}" does not exist!')
    
    with open(request.json['path'], 'r' ) as file:
        dix = json.load(file)

    return make_json_response(dix)

@app.route('/edit-shortcuts', methods=['POST', 'GET'])
def edit_shortcuts():
    # Expecting the following keys
    # summary options and chat package
    # request.json should be in format of apiutils/samples/sample_api_request_1.json
    if request.json is None:
        return error_response(400, message='No JSON content included!')
    
    versionFolder = os.path.split(request.json['updatesPath'])[0]

    # load the updates file into the dictionary
    with open(os.path.join(versionFolder, 'updates.json'), 'r' ) as file:
        testUpdates = json.load(file)

    idMapper = {}

    for sc in testUpdates['children']:
        idMapper[sc['id']] = sc

    for sc in request.json['shortcuts']:
        idMapper[sc['id']]['version'] = sc['version']
        idMapper[sc['id']]['link'] = sc['link']

        # edit the version comment shortcuts py file
        pyfile = idMapper[sc['id']]['pyfile']
        pyfile = os.path.join(REPO, '\\'.join(pyfile.split('/')))
        with open(pyfile, 'r') as file:
            lines = file.readlines()

        lines[3] = 'Ver: {}\n'.format(sc['version'])

        with open(pyfile, 'w') as file:
            file.writelines(lines)
        

    # write it to test updates
    with open(os.path.join(versionFolder, 'testupdates.json'), 'w' ) as file: 
        json.dump(testUpdates, file, indent=4)

    
    # then create the child vers which we are sending back
    verMap = { sc['id']: sc['version'] for sc in testUpdates['children']}
    dix = {
        'verMap' : json.dumps(verMap)
    }

    return make_json_response(dix)

@app.route('/update-installer', methods=['POST', 'GET'])
def update_installer():

    # read from the test updates file and use the version numbers in there
    versionFolder = os.path.split(request.json['updatesPath'])[0]

    # load the updates file into the dictionary
    with open(os.path.join(versionFolder, 'testupdates.json'), 'r' ) as file:
        testUpdates = json.load(file)

    with open(os.path.join(versionFolder, 'updates.json'), 'r' ) as file:
        updates = json.load(file)

    installer = os.path.join(REPO, '\\'.join(testUpdates['pyfile'].split('/')))

    with open(installer, 'r') as file: 
        text = file.read()

    # replace the old version number with the new version number in installer
    for old, new in zip(updates['children'], testUpdates['children']):
        text = text.replace(
            '"{}":"{}"'.format(old['id'], old['version']),
            '"{}":"{}"'.format(new['id'], new['version'])
        )

    # replace new framework version in installer
    text = text.replace(
        "'version':'{}'".format(updates['version']),
        "'version':'{}'".format(request.json['version'])
    )

    # set new values in test updates
    testUpdates['version'] = request.json['version']
    testUpdates['link'] = request.json['link']


    with open(installer, 'w') as file: 
        file.write(text)

    with open(os.path.join(versionFolder, 'testupdates.json'), 'w' ) as file:
        json.dump(testUpdates, file, indent=4)

    return make_json_response({'message': 'Completed!'})

@app.route('/update-release-notes', methods=['POST', 'GET'])
def update_release_notes():

    # read from the test updates file and use the version numbers in there
    versionFolder = os.path.split(request.json['updatesPath'])[0]

    # load the updates file into the dictionary
    with open(os.path.join(versionFolder, 'testupdates.json'), 'r' ) as file:
        testUpdates = json.load(file)

    testUpdates['releaseNotes'] = request.json['releaseNotes']
    testUpdates['releaseTime'] = datetime.today().strftime('%Y-%m-%d')

    with open(os.path.join(versionFolder, 'testupdates.json'), 'w' ) as file:
        json.dump(testUpdates, file, indent=4)

    return make_json_response({'message': 'Completed!'})

@app.route('/promotion', methods=['POST', 'GET'])
def promotion():

    # read from the test updates file and use the version numbers in there
    versionFolder = os.path.split(request.json['updatesPath'])[0]

    # load the updates file into the dictionary
    with open(os.path.join(versionFolder, 'testupdates.json'), 'r' ) as file:
        testUpdates = json.load(file)

    with open(os.path.join(versionFolder, 'updates.json'), 'r' ) as file:
        updates = json.load(file)

    with open(os.path.join(versionFolder, 'history.json'), 'r' ) as file:
        history = json.load(file)

    # push current updates version into history
    history.insert(0, updates)

    # write test updates and history
    with open(os.path.join(versionFolder, 'updates.json'), 'w' ) as file:
        json.dump(testUpdates, file, indent=4)

    with open(os.path.join(versionFolder, 'history.json'), 'w' ) as file:
        json.dump(history, file, indent=4)

    return make_json_response({'message': 'Completed!'})

# running the code
if __name__ == '__main__':
    # debug is true to show errors on the webpage
    app.run(debug=True)