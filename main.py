import os
import csv
import sys, getopt
from load_block_model import loadModelArguments, printModelArguments, numberOfBlocksArguments, massInKilogramsArgument, gradeInPercentageArguments, attributeArguments, reblockArguments, LoadBlockModel, CreateBlockModel, apiReblockModel
from flask import Flask, json, flash, request, redirect, url_for, Response
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from flask_api import status
import json
import csv

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'blocks', 'txt'}

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

def show_blocks(name):
    filename = name + "_blocks_reblock.csv"

    if not os.path.exists(filename):
        filename = name + "_blocks.csv"

    with open(filename, 'r') as csv_file:
        lines = csv_file.readlines()
        offset = 3 + int(lines[3])

        blocks = []
        columns = []

        for line in range(len(lines)):
            block = {}
            if line == 0:
                columns = lines[line].strip().split(",")
            elif line > offset:
                current_block = lines[line].strip().split(",")
                for i in range(len(columns)):
                    if (str(columns[i]) == "id"):
                        block['index'] = current_block[i]
                    else:
                        block[str(columns[i])] = current_block[i]
                blocks.append(block)
        return blocks

@app.route('/')
def hello():
    status_code = {status.HTTP_200_OK:  'OK'}
    return status_code


@app.route('/api/block_models/load_model/', methods=['GET', 'POST'])
def load_block_model():
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
            return status_code
    return status_code
    

@app.route('/api/block_models/<name>/reblock/<x>/<y>/<z>', methods=['GET'])
def reblock_model(name, x, y, z):
    
    status_code = {status.HTTP_200_OK:  'OK'}

    inputfile = name + "_blocks_reblock.csv"

    if not os.path.exists(inputfile):
        inputfile = name + "_blocks.csv"
    
    apiReblockModel(inputfile, x, y, z)

    return status_code


@app.route('/api/block_models/', methods=['GET'])
def block_models():
    directory = os.getcwd()
    names = []

    status_code = {status.HTTP_200_OK:  'OK'}

    for filename in os.listdir(directory):
        name_extension = []
        if filename.endswith(".csv"):
            names.append({ 'name': filename.split("_blocks")[0] })
    return json.dumps(names), status_code


@app.route('/api/block_models/<name>/blocks/')
def loaded_blocks(name):
    status_code = {status.HTTP_200_OK:  'OK'}
    return json.dumps(show_blocks(name)), status_code


@app.route('/api/block_models/<name>/blocks/<index>/')
def index_block(name, index):
    status_code = {status.HTTP_200_OK:  'OK'}
    model = show_blocks(name)
    for i in model:
        print(i['index'])
        if int(i['index']) == int(index):
            block = i
    return json.dumps({"block": block}), status_code


if __name__ == "__main__":
    #app.run(port=8001)
    
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(port=5000)
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