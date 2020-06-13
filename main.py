import os
import csv
import sys, getopt
from load_block_model import loadModelArguments, printModelArguments, numberOfBlocksArguments, massInKilogramsArgument, gradeInPercentageArguments, attributeArguments, reblockArguments, getModelNames, getModelBlock, getBlockModelObject
from flask import Flask, jsonify
from flask_cors import CORS
import json
import csv
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    text = 'Hello World'
    return requests.get('https://dry-brushlands-69779.herokuapp.com/api/feature_flags/').json


@app.route('/api/block_models/', methods=['GET'])
def block_models():
    ff = requests.get('https://dry-brushlands-69779.herokuapp.com/api/feature_flags/').json()
    names = getModelNames()
    if ff['restful_response']:
        return json.dumps({'block_models': names})
    return json.dumps(names)


@app.route('/api/block_models/<name>/blocks/', methods=['GET'])
def loaded_blocks(name):
    ff = requests.get('https://dry-brushlands-69779.herokuapp.com/api/feature_flags/').json()
    blocks = getBlockModelObject(name, ff['restful_response'])
    return json.dumps(blocks)


@app.route('/api/block_models/<name>/blocks/<index>/', methods=['GET'])
def index_block(name, index):
    ff = requests.get('https://dry-brushlands-69779.herokuapp.com/api/feature_flags/').json()
    if ff['block_info']:
        block = getModelBlock(name, index)
        return json.dumps({"block": block})


if __name__ == "__main__":
    #app.run(port=8001)
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