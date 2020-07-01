import os
import csv
import sys, getopt
from load_block_model import *
from flask import Flask, flash, request, redirect, url_for, Response, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from flask_api import status
import json
import csv
import requests

app = Flask(__name__)
CORS(app)
#span_id = None

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'blocks', 'txt', 'prec'}

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/block_models/load_model/', methods=['GET', 'POST'])
def load_block_model():
    #global span_id
    status_code = {status.HTTP_200_OK:  'OK'}
    if request.method == 'POST':
        if 'blocks' not in request.files or 'columns' not in request.files:
            flash('No file part')
            return redirect(request.url)
        blocks = request.files['blocks']
        columns = request.files['columns']
        if blocks.filename == '' or columns.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if blocks and columns and allowed_file(blocks.filename) and allowed_file(columns.filename):
            blocks_filename = secure_filename(blocks.filename)
            blocks.save(os.path.join(app.config['UPLOAD_FOLDER'], blocks_filename))
            columns_filename = secure_filename(columns.filename)
            columns.save(os.path.join(app.config['UPLOAD_FOLDER'], columns_filename))
            LoadBlockModel(blocks.filename, columns.filename)
            span_id = getSpanId() + 1
            requests.post('https://gentle-coast-69723.herokuapp.com/api/apps/efd22a06b2110e39cdd1031c7fbc48bb/traces/',
                          json={"trace": {"span_id": span_id, "event_name": "block_model_loaded",
                                          "event_data": blocks.filename.split('.')[0]}})
            return status_code
    return status_code


@app.route('/api/block_models/<name>/load_prec', methods=['GET', 'POST'])
def load_prec_model(name):
    #global span_id
    status_code = {status.HTTP_200_OK: 'OK'}
    if request.method == 'POST':
        prec = request.files['prec']
        if prec.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if prec and allowed_file(prec.filename):
            prec_filename = secure_filename(prec.filename)
            span_id = getSpanId()
            requests.post('https://gentle-coast-69723.herokuapp.com/api/apps/efd22a06b2110e39cdd1031c7fbc48bb/traces/',
                          json={"trace": {"span_id": span_id, "event_name": "block_model_precedences_loaded",
                                          "event_data": prec.filename.split('.')[0]}})
            prec.save(os.path.join(app.config['UPLOAD_FOLDER'], prec_filename))
            return status_code
    return status_code


@app.route('/api/block_models/<name>/reblock/<x>/<y>/<z>', methods=['GET'])
def reblock_model(name, x, y, z):
    #global span_id
    status_code = {status.HTTP_200_OK:  'OK'}

    inputfile = name + "_blocks_reblock.csv"

    if not os.path.exists(inputfile):
        inputfile = name + "_blocks.csv"
    
    apiReblockModel(inputfile, x, y, z)
    span_id = getSpanId()
    requests.post('https://gentle-coast-69723.herokuapp.com/api/apps/efd22a06b2110e39cdd1031c7fbc48bb/traces/',
                  json={"trace": {"span_id": span_id, "event_name": "block_model_reblocked",
                                  "event_data": name}})
    return status_code


@app.route('/api/block_models/', methods=['GET'])
def block_models():
    ff = requests.get('https://dry-brushlands-69779.herokuapp.com/api/feature_flags/').json()
    names = getModelNames()
    if ff['restful_response']:
        return json.dumps({'block_models': names})
    return json.dumps(names)


@app.route('/api/block_models/<name>/blocks/', methods=['GET'])
def loaded_blocks(name):
    #global span_id
    ff = requests.get('https://dry-brushlands-69779.herokuapp.com/api/feature_flags/').json()
    blocks = getBlockModelObject(name, ff['restful_response'])
    span_id = getSpanId()
    requests.post('https://gentle-coast-69723.herokuapp.com/api/apps/efd22a06b2110e39cdd1031c7fbc48bb/traces/',
                  json={"trace": {"span_id": span_id, "event_name": "blocks_requested",
                                  "event_data": name}})
    return json.dumps(blocks)


@app.route('/api/block_models/<name>/blocks/<index>/', methods=['GET'])
def index_block(name, index):
    #global span_id
    ff = requests.get('https://dry-brushlands-69779.herokuapp.com/api/feature_flags/').json()
    if ff['block_info']:
        block = getModelBlock(name, index)
        span_id = getSpanId()
        requests.post('https://gentle-coast-69723.herokuapp.com/api/apps/efd22a06b2110e39cdd1031c7fbc48bb/traces/',
                      json={"trace": {"span_id": span_id, "event_name": "block_info_requested",
                                      "event_data": "<{}>,<{}>,<{}>".format(block['x'], block['y'], block['z'])}})
        return json.dumps({"block": block})

@app.route('/api/block_models/<name>/blocks/<index>/extract/', methods=['POST'])
def extract_block(name, index):
    global span_id
    filename = name + "_blocks.csv"

    block_model = CreateBlockModel(filename)
    AddPrecedenceToBlockModel(block_model, name)

    selected_block = block_model.getBlockById(index)
    extracted = extract(selected_block)
    blo = {'x': selected_block.getValue("x"), 'y': selected_block.getValue("y"), 'z': selected_block.getValue("z")}
    span_id = getSpanId()
    requests.post('https://gentle-coast-69723.herokuapp.com/api/apps/efd22a06b2110e39cdd1031c7fbc48bb/traces/',
                  json={"trace": {"span_id": span_id, "event_name": "block_extracted",
                                  "event_data": "<{}>,<{}>,<{}>".format(blo['x'], blo['y'], blo['z'])}})
    return json.dumps({"blocks": extracted})

if __name__ == "__main__":
    app.secret_key = "SUPER SECRET KEY"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=8001)
    #app.run(port=5000)
    if sys.argv[1] == '-L':
        print(loadModelArguments(sys.argv[2:]))
    elif sys.argv[1] == '-P':
        printModelArguments(sys.argv[2:])
    elif sys.argv[1] == '-N':
        print(numberOfBlocksArguments(sys.argv[2:]))
    elif sys.argv[1] == '-M':
        print(massInKilogramsArgument(sys.argv[2:]))
    elif sys.argv[1] == '-G':
        print(gradeInPercentageArguments(sys.argv[2:]))
    elif sys.argv[1] == '-A':
        print(attributeArguments(sys.argv[2:]))
    elif sys.argv[1] == '-R':
        print(reblockArguments(sys.argv[2:]))
    elif sys.argv[1] == '-E':
        print()
        # print(extractArguments(sys.argv[2:]))
    else:
        print('\nAvailable commands:\n')
        print('main.py -L -i <inputfile> -c <columnsFile>')
        print('Load file. Needs input file name and output file name.')
        print('----')
        print('main.py -P -i <inputfile>')
        print('Print file. Needs input file name.')
        print('----')
        print('main.py -N  -b <block_model_name>')
        print('Number of Blocks of a stored block model. Needs block model name and number of blocks.')
        print('----')
        print('main.py -M -b <block_model_name> -x <block_x> -y <block_y> -z <block_z>')
        print('Mass in Kilograms of one block in a stored block model. Needs block model name and coordinates.')
        print('----')
        print('main.py -G -b <block_model_name> -x <block_x> -y <block_y> -z <block_z> -m <mineral_name>')
        print('Grade in Percentage for each Mineral of one block in a stored block model. Needs block model name, coordinates and mineral name.')
        print('----')
        print('main.py -A -b <block_model_name> -x <block_x> -y <block_y> -z <block_z> -n <attribute_name>')
        print('Search attribute of one block in a stored block model. Needs block model name, coordinates and attribute name.')
        print('----')
        print('main.py -R -i <inputfile> -x <xreblock> -y <yreblock> -z <zreblock>')
        print('Reblock the model by merging blocks after the dimensions indicated.')