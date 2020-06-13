import os
import csv
import sys, getopt
from block import Block
from block_model import BlockModel
from collections import defaultdict

def loadModelArguments(argv):
    inputfile = ''
    columnsfile = ''
    try:
        opts, args = getopt.getopt(argv,"i:c:",["ifile=", "cfile="])
    except getopt.GetoptError:
        print('main.py -L -i <inputfile> -c <columnsFile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-c", "--cfile"):
            columnsfile = arg

    return LoadBlockModel(inputfile, columnsfile)

def printModelArguments(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"i:",["ifile="])
    except getopt.GetoptError:
        print('main.py -P -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
    
    blockModel = CreateBlockModel(inputfile)
    PrintBlockModel(blockModel)


def numberOfBlocksArguments(argv):
    block_model_name = ""

    try:
        opts, args = getopt.getopt(argv, "b:", ["bname="])
    except getopt.GetoptError:
        print('main.py -N -b <block_model_name>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-b", "--bname"):
            block_model_name = arg

    block_model = CreateBlockModel(block_model_name)
    return printNumberOfBlocks(block_model)

def massInKilogramsArgument(argv):
    block_model_name = ""
    x = 0
    y = 0
    z = 0

    try:
        opts, args = getopt.getopt(argv, "b:x:y:z:", ["bname=", "xcoord=", "ycoord=", "zcoord="])
    except getopt.GetoptError:
        return 'main.py -M <block_model_name> <block_x> <block_y> <block_z>'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-b", "--bname"):
            block_model_name = arg
        elif opt in ("-x", "--xcoord"):
            x = int(arg)
        elif opt in ("-y", "--ycoord"):
            y = int(arg)
        elif opt in ("-z", "--zcoord"):
            z = int(arg)

    block_model = CreateBlockModel(block_model_name)
    return printMassInKilograms(block_model, x, y, z)

def gradeInPercentageArguments(argv):
    block_model_name = ""
    x = 0
    y = 0
    z = 0
    mineral_name = ""

    try:
        opts, args = getopt.getopt(argv, "b:x:y:z:m:", ["bname=", "xcoord=", "ycoord=", "zcoord=", "mname="])
    except getopt.GetoptError:
        return 'main.py -G -b <block_model_name> -x <block_x> -y <block_y> -z <block_z> -m <mineral_name>'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-b", "--bname"):
            block_model_name = arg
        elif opt in ("-x", "--xcoord"):
            x = int(arg)
        elif opt in ("-y", "--ycoord"):
            y = int(arg)
        elif opt in ("-z", "--zcoord"):
            z = int(arg)
        elif opt in ("-m", "--mname"):
            mineral_name = arg

    blocks = CreateBlockModel(block_model_name)
    return GetGradeOfMineral(blocks, x, y, z, mineral_name)

def attributeArguments(argv):
    block_model_name = ""
    x = 0
    y = 0
    z = 0
    attribute_name = ""

    try:
        opts, args = getopt.getopt(argv, "b:x:y:z:n:", ["bname=", "xcoord=", "ycoord=", "zcoord=", "aname="])
    except getopt.GetoptError:
        return 'main.py -A -b <block_model_name> -x <block_x> -y <block_y> -z <block_z> -n <attribute_name>'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-b", "--bname"):
            block_model_name = arg
        elif opt in ("-x", "--xcoord"):
            x = int(arg)
        elif opt in ("-y", "--ycoord"):
            y = int(arg)
        elif opt in ("-z", "--zcoord"):
            z = int(arg)
        elif opt in ("-n", "--aname"):
            attribute_name = arg

    blocks = CreateBlockModel(block_model_name)
    return GetAttribute(blocks, x, y, z, attribute_name)

def CreateBlockModel(input_name):
    blocks = []
    mass = ""
    n_minerals = 1
    minerals = {}
    columns = []
    classification = []
    block_map = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    block_values = []

    with open(input_name, 'r') as csv_block_file:
        lines = csv_block_file.readlines()
        for line in range(len(lines)):  
            if line == 0:
                columns = lines[line].strip().split(',')
            elif line == 1:
                classification = list(map(int, lines[line].strip().split(',')))
            elif line == 2:
                mass = lines[line].strip()
            elif line == 3:
                n_minerals = int(lines[line].strip())
            elif line in range(4, 4 + n_minerals):
                MINERAL_COLUMN = 0
                MINERAL_NAME = 1
                MINERAL_UNIT = 2
                mineral_info = lines[line].strip().split(',')
                minerals[mineral_info[MINERAL_NAME]] = [mineral_info[MINERAL_UNIT], mineral_info[MINERAL_COLUMN]]
            else:
                block_values = lines[line].strip().split(',')
                block = Block(columns, mass, minerals, block_values, classification)
                blocks.append(block)
                try:
                    block_x = str(block_values[columns.index("x")])
                except:
                    block_x = str(block_values[columns.index("<x>")])
                try:
                    block_y = str(block_values[columns.index("y")])
                except:
                    block_y = str(block_values[columns.index("<y>")])
                try:
                    block_z = str(block_values[columns.index("z")])
                except:
                    block_z = str(block_values[columns.index("<z>")])
                block_map[block_x][block_y][block_z] = block
    return BlockModel(columns, blocks, block_map)

def LoadBlockModel(input_name, columns_name):
    print("loading...")
    block_file = open(input_name, "r")
    lines = block_file.readlines()
    block_file.close()

    columns_file = open(columns_name, "r")
    columns = columns_file.readlines()
    columns_file.close()

    input_name = input_name.split('.')
    output_name = input_name[0] + "_" + input_name[1] + ".csv"

    with open(output_name, 'w', newline='') as csv_block_file:
        wr = csv.writer(csv_block_file, quoting=csv.QUOTE_MINIMAL)
        for column in columns:
            wr.writerow(column.strip().split(','))
        for line in lines:
            csv_line = line.split()
            for i in range(len(csv_line)):
                try:
                    csv_line[i] = int(csv_line[i])
                except:
                    try:
                        csv_line[i] = float(csv_line[i])
                    except:
                        csv_line[i] = str(csv_line[i])
            wr.writerow(csv_line)

    return 1

def PrintBlockModel(block_model):

    elements = []
    max_element_length = []

    elements.append(block_model.columns)

    for x in range(len(block_model.blocks)):
        elements.append(block_model.blocks[x].values)

    for n in range(len(elements[0])):
        max_element_length.append(0)

    for i in range(len(elements)):
        for j in range(len(elements[0])):
            if len(elements[i][j]) > max_element_length[j]:
                max_element_length[j] = len(str(elements[i][j]))

    print(' ' + '-'*(sum(max_element_length) + len(max_element_length) - 1))

    for i in range(len(elements)):
        values = '|'
        for j in range(len(elements[0])):
            element = elements[i][j].strip()

            values += str(element) + (" "*int(max_element_length[j]-len(str(element)))) + '|'
        print(values)
        print(' ' + '-'*(sum(max_element_length) + len(max_element_length) - 1))


def GetAttribute(block_model, X, Y, Z, attribute_name):
    block = block_model.getBlock(X, Y, Z)
    if type(block) is str:
        return block
    else:
        return block.getValue(attribute_name)

def GetGradeOfMineral(block_model, X, Y, Z, mineral_name):
    block = block_model.getBlock(X, Y, Z)
    if type(block) is str:
        return block
    else:
        return block.getMineralGrade(mineral_name)

def printNumberOfBlocks(block_model):
    number_of_blocks = len(block_model.blocks)

    return number_of_blocks

def printMassInKilograms(block_model, x, y, z):
    block = block_model.getBlock(x, y, z)
    if type(block) is str:
        return block
    else:
        possible_names = ["<tonn>", "ton", "tonns", "tons", "rock_tonnes"]
        
        for name in possible_names:
            if name in block_model.columns:
                mass = float(block.getValue(name))*1000
                return str(mass) + "kg"
    

def reblockArguments(argv):
    rx = ""
    ry = ""
    rz = ""
    inputfile = ""
    try:
        opts, args = getopt.getopt(argv, "i:x:y:z:", ["ifile=", "xcoord=", "ycoord=", "zcoord="])
    except getopt.GetoptError:
        print('main.py -R -i <inputfile> -x <xreblock> -y <yreblock> -z <zreblock>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-x", "--xcoord"):
            rx = arg
        elif opt in ("-y", "--ycoord"):
            ry = arg
        elif opt in ("-z", "--zcoord"):
            rz = arg


    blockModel = CreateBlockModel(inputfile)
    blocks = blockModel.reBlock(int(rx), int(ry), int(rz))

    original_file = open(inputfile, 'r')
    model_name = inputfile.split('.')[0]
    reblock_file = open(model_name+'_reblock.csv', 'w', newline='')

    column_line = original_file.readline()
    reblock_file.writelines(column_line)
    classification_line = original_file.readline()
    reblock_file.write(classification_line)
    mass_line = original_file.readline()
    reblock_file.writelines(mass_line)
    minerals_amount_line = original_file.readline()
    reblock_file.writelines(minerals_amount_line)

    minerals_amount = int(minerals_amount_line)
    for mineral in range(minerals_amount):
        reblock_file.writelines(original_file.readline())

    original_file.close()

    for x in blocks:
        for y in x:
            for block in y:
                if block is None:
                    continue
                line = ""
                for i in range(len(block.values)-1):
                    line += str(block.values[i]) + ','
                line += str(block.values[-1]) + '\n'
                reblock_file.writelines(line)
    
    reblock_file.close()

    print(len(blocks), len(blocks[0]), len(blocks[0][0]))

def apiReblockModel(inputfile, x, y, z):
    block_model = CreateBlockModel(inputfile)
    blocks = block_model.reBlock(int(x), int(y), int(z))

    original_file = open(inputfile, 'r')
    model_name = inputfile.split('.')[0]
    reblock_file = open(model_name+'_reblock.csv', 'w', newline='')

    column_line = original_file.readline()
    reblock_file.writelines(column_line)
    classification_line = original_file.readline()
    reblock_file.write(classification_line)
    mass_line = original_file.readline()
    reblock_file.writelines(mass_line)
    minerals_amount_line = original_file.readline()
    reblock_file.writelines(minerals_amount_line)

    minerals_amount = int(minerals_amount_line)
    for mineral in range(minerals_amount):
        reblock_file.writelines(original_file.readline())

    original_file.close()

    for x in blocks:
        for y in x:
            for block in y:
                if block is None:
                    continue
                line = ""
                for i in range(len(block.values)-1):
                    line += str(block.values[i]) + ','
                line += str(block.values[-1]) + '\n'
                reblock_file.writelines(line)
    
    reblock_file.close()

def getModelNames():
    directory = os.getcwd()
    names = []

    for filename in os.listdir(directory):
        name_extension = []
        if filename.endswith("_blocks.csv"):
            names.append({ 'name': filename.split("_blocks")[0] })
        elif filename.endswith('_reblock.csv'):
            names.append({ 'name': filename.split("_blocks")[0] + '_reblocked' })

    return names


def getModelBlock(name, index):
    blocks = getBlockModel(name)

    block = {}
    for i in blocks:
        if int(index) == int(i.getValue('id')):
            block['index'] = index
            block['x'] = i.getValue('x')
            block['y'] = i.getValue('y')
            block['z'] = i.getValue('z')
            minerals = {}
            for j in i.minerals:
                minerals[j] = i.getMineralGrade(j)
            block['grades'] = minerals
            block['mass'] = i.getValue(i.mass)
            break
    return block


def getBlockModelObject(name, restful):
    blocks = getBlockModel(name)

    new_blocks = []
    for i in range(len(blocks)):
        block = {}
        for j in range(len(blocks[i].columns)):
            if blocks[i].columns[j] == 'id':
                block['index'] = blocks[i].values[j]
            else:
                block[blocks[i].columns[j]] = blocks[i].values[j]
        new_blocks.append(block)
    
    if restful:
        return {'block_model': {'blocks': new_blocks}}
    return new_blocks


def getBlockModel(name):
    if name.endswith('_reblocked'):
        filename = name.split('_reblocked')[0] + "_blocks_reblock.csv"
    else:
        filename = name + "_blocks.csv"

    blockModel = CreateBlockModel(filename)
    nBlocks = printNumberOfBlocks(blockModel)
    if nBlocks > 5000:
        if nBlocks < 25000:
            blockModel = blockModel.reBlock(2, 2, 2)
        elif nBlocks >= 25000:
            blockModel = blockModel.reBlock(3, 3, 3)

        reblocks = []
        for i in blockModel:
            for j in i:
                for k in j:
                    if k != None:
                        reblocks.append(k)
        return reblocks

    blocks = []
    for i in blockModel.blocks:
        blocks.append(i)
    return blocks
