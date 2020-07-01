# group_2_2020

# To Build:

Just clone this repository into your computer.
Be sure to have your kb.blocks in the same folder as your main.py and test_main.py files.
All modules required (os, unittest, csv, sys, getopt) should come with python 3.


# To Test:

There are some files that have tests created i.e. (test_block, test_block_model, test_load_block_model, etc).
To run this tests just type in the command console the following command (be sure to have your console in the correct directory):

- run all tests: python -m unittest

- run a specific test: python -m unittest test_name

# Web API:

To be able to successfuly use the Web API, you have to first load the block models you want to use (refer to documentation on how to load block models into this application). 
Reblocked models of the same model have priority over the original ones

/api/block_models/load_model/ -> two files need to be uploaded through Postman. In the Body option, choose form-data and enter two files: with the key "columns" upload the columns file (.txt) and with the key "blocks", the model file (.blocks).

/api/block_models/{ModelName}/load_prec -> one file needs to be uploaded through Postman. In the Body option, choose form-data and enter one file: with the key "prec" upload the precedents file (.prec).

IMPORTANT: the columns file must follow the following structure:  
- first line: columns (attributes) of the model separated by comas.  
- second line: classification of the attributes separated by comas. 0 = summable value, 1 = proportional value, 2 = mode.  
- third line: column name of the mass.  
- fourth line: integer representing the n amount of minerals.  
- fifth to n-lines more: column name of the mineral, common name of the mineral and metric.

# To Use:

There are 6 main console commands that can be used in this program.

1. Load Block Model:

    The following command is used to load the block model and saves it into a csv file (be sure to use a .csv as the outputFile name).

    main.py -L -i [inputFile] -c [columnsFile.txt]

    i.e.

    main.py -L -i kd.blocks -c columns.txt

    IMPORTANT: the columns file must follow the following structure:
    - first line: columns (attributes) of the model separated by comas.
    - second line: classification of the attributes separated by comas. 0 = summable value, 1 = proportional value, 2 = mode.
    - third line: column name of the mass.
    - fourth line: integer representing the n amount of minerals.
    - fifth to n-lines more: column name of the mineral, common name of the mineral and metric.

    i.e.  
  
    id,x,y,z,tonn,blockvalue,destination,Au (oz/ton),Ag (oz/ton),Cu %  
    0,0,0,0,0,0,2,1,1,1 
    tonn>
    3  
    Cu %,copper,%  
    Au (oz/ton),gold,oz/ton  
    Ag (oz/ton),silver,oz/ton  

2. Print a previously saved block model:

    The following command is used to print a previously saved block model in a .csv file:

    main.py -P -i [blockModelFile.csv]

    i.e.

    main.py -P -i kd_blocks.csv

3. Print number of blocks in a previously saved model:

    The following command is used to print the number of blocks in a block model that was prevoiusly loaded:

    main.py -N -b [blockModelFile.csv]

    i.e.

    main.py -N -b kd_blocks.csv

4. Print mass in Kilograms of one block in a stored block model:

    The following command is used to print the mass in kilograms of a block stored in a block model previously loaded in a specific coordinate:

    main.py -M -b [blockModelFile.csv] -x [xCoordinate] -y [yCoordinate] -z [zCoordinate]

    i.e.

    main.py -M -b kd_blocks.csv -x 11 -y 0 -z 18

5. Print grade in percentage for each mineral of one block in a stored block model:

    The following command is used to print the grade in percentage for a mineral in a block of a previously loaded block model in a specific coordinate:

    main.py -G -b [blockModelFile.csv] -x [xCoordinate] -y [yCoordinate] -z [zCoordinate] -m [mineralName]

    i.e.

    main.py -G -b kd_blocks.csv -x 11 -y 0 -z 18 -m copper

6. Print value of attribute of one block in a stored block model:

    The following command is used to print the value of any attribute in a previously stored block model in a specific coordinate:

    main.py -A -b [blockModelFile.csv] -x [xCoordinate] -y [yCoordinate] -z [zCoordinate] -n "[attributeName]"

    i.e.

    main.py -A -b kd_blocks.csv -x 11 -y 0 -z 12 -n "destination"

7. Reblock the model by merging blocks:

    The following command is used to reblock a previously stored block model. The amount of merged blocks into one is the product between the given dimensions in the command line.

    main.py -R -i [inputfile] -x [xreblock] -y [yreblock] -z [zreblock]

    i.e.

    main.py -R -i kd_blocks.csv -x 2 -y 3 -z 2
