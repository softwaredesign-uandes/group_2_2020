class Block:
    def __init__(self, columns, mass, minerals, values, classification):
        self.columns = columns
        self.mass = mass
        self.minerals = minerals
        self.values = values
        self.classification = classification
        self.precedence = []

    #Fix this with new parameters
    def __eq__(self, other):
        try:
            if len(self.columns) != len(other.columns):
                return False
            if len(self.values) != len(other.values):
                return False
            for list_index in range(len(self.columns)):
                if not(self.columns[list_index] == other.columns[list_index]):
                    return False
                if self.classification[list_index] == 2:
                    continue
                if not(self.values[list_index] == other.values[list_index]):
                    return False
            return True
        except:
            return False

    def getValue(self, column):
        try:
            return self.values[self.columns.index(column)]
        except:
            return "Column does not exist"

    def getMineralGrade(self, mineral):
        MINERAL_UNIT = 0
        MINERAL_COLUMN = 1
        OZ_TON_TO_GRAMS = 28.3495
        mineral_column_name = ""
        mineral_value = 0.0
        if mineral in self.minerals.keys():
            mineral_column_name = self.minerals[mineral][MINERAL_COLUMN]
            try:
                mineral_value = float(self.values[self.columns.index(mineral_column_name)])
            except:
                return "Column of the mineral does not match any of the existing columns"
            if self.minerals[mineral][MINERAL_UNIT] == "%":               
                return mineral_value
            elif self.minerals[mineral][MINERAL_UNIT] == "oz/ton":
                return (mineral_value * OZ_TON_TO_GRAMS / 10000)
            elif self.minerals[mineral][MINERAL_UNIT] == "ppm":
                return float(mineral_value) / 10000
            elif self.minerals[mineral][MINERAL_UNIT] == "tonn":
                return (100 * float(mineral_value) / float(self.values[self.columns.index(self.mass)]))
            else:
                return "Unit of meassurement not recognised"           
        else:
            return "Mineral does not exist in this model"

    
    def getValueClassificationPair(self, column):
        try:
            column_index = self.columns.index(column)
            return (self.values[column_index], self.classification[column_index])
        except:
            return "Column does not exist"