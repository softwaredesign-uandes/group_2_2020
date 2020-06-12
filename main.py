import os
import csv
import sys, getopt
from load_block_model import loadModelArguments, printModelArguments, numberOfBlocksArguments, massInKilogramsArgument, gradeInPercentageArguments, attributeArguments, reblockArguments
from flask import Flask
from flask_cors import CORS
import json
import csv

app = Flask(__name__)
CORS(app)

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
                    block[str(columns[i])] = current_block[i]
                blocks.append(block)
        return blocks

@app.route('/')
def hello():
    text = 'Hello World'
    return text


@app.route('/api/block_models/', methods=['GET'])
def block_models():
    directory = os.getcwd()
    names = []

    for filename in os.listdir(directory):
        name_extension = []
        if filename.endswith(".csv"):
            names.append({ 'name': filename.split("_blocks")[0] })
    return json.dumps(names_output)


@app.route('/api/block_models/<name>/blocks/')
def loaded_blocks(name):
    out = show_blocks(name)
    return json.dumps({"block_model": {"blocks": out}})


@app.route('/api/block_models/<name>/blocks/<index>/')
def index_block(name, index):
    model = show_blocks(name)
    block = model[int(index)]
    return json.dumps({"block": block})


if __name__ == "__main__":
    app.run(port=8001)
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