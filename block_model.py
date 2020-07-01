from reblock_functions import *
import math

class BlockModel:
    def __init__(self, columns, blocks, blocks_map):
        self.columns = columns
        self.blocks = blocks
        self.blocks_map = blocks_map

    def __eq__(self, other):
        try:
            if len(self.blocks) != len(other.blocks):
                return False
            if len(self.columns) != len(other.columns):
                return False
            for n in range(len(self.columns)):
                if not(self.columns[n] == other.columns[n]):
                    return False
            for i in range(len(self.blocks)):
                if not(self.blocks[i].__eq__(other.blocks[i])):
                    return False
            return True
        except:
            return False

    def getBlock(self, X, Y, Z):
        block = self.blocks_map[str(X)][str(Y)][str(Z)]
        if type(block) is int:
            return "Block does not exist"
        else:
            return block

    def getBlockById(self, id):
        
        id_column_index = 0
        i = 0
        while i < len(self.columns):
            if "id" in self.columns[i].lower():
                id_column_index = i
                break
            i += 1

        for block in self.blocks:
            if block.values[id_column_index] == id:
                return block
        
        return None

    def reBlock(self, rx, ry, rz):
        if invalidParameters([rx, ry, rz]):
            return "Invalid parameters"
        x = 0
        y = 0
        z = 0
        for block in self.blocks:
            try:
                if int(block.getValue("x")) > x:
                    x = int(block.getValue("x"))
            except:
                if int(block.getValue("<x>")) > x:
                    x = int(block.getValue("<x>"))
            try:
                if int(block.getValue("y")) > y:
                    y = int(block.getValue("y"))
            except:
                if int(block.getValue("<y>")) > y:
                    y = int(block.getValue("<y>"))
            try:
                if int(block.getValue("z")) > z:
                    z = int(block.getValue("z"))
            except:
                if int(block.getValue("<z>")) > z:
                    z = int(block.getValue("<z>"))

        x+=1
        y+=1
        z+=1
        new_x = math.ceil(x / float(rx))
        new_y = 0
        if not new_x == new_y:
            new_y = math.ceil(y / float(ry))
        new_z = 0
        if not new_y == new_z:
            new_z = math.ceil(z / float(rz))

        new_blocks = emptyblocks(new_x, new_y, new_z)
        count_x = 0
        count_y = 0
        count_z = 0
        for i in range(0, x, rx):
            count_y = 0
            for j in range(0, y, ry):
                count_z = 0
                for k in range(0, z, rz):
                    new_blocks[count_x][count_y][count_z] = reblockAroundBlocks(self, i, j, k, rx, ry, rz)
                    count_z += 1
                count_y += 1
            count_x += 1
        return new_blocks


