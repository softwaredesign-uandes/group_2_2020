import unittest
from block import Block
from block_model import BlockModel
from load_block_model import *

class TestLoadBlockModel(unittest.TestCase):

    # test para obtener el grade de algun mineral es el mismo que en test_block ya que llama a dicha funcion para un
    # bloque en especifico
    # La mayoria de las funciones llaman a funciones propias de block y block model por lo que sus respectivos test
    # estan en sus respectivos archivos
    def test_create_block_model_when_csv_exists_return_block_model(self):
        # columns = ['<id>', '<x>', '<y>', '<z>', '<tonn>', '<destination>', '<Au (oz/ton)>', '<Ag [ppm]>', '<Cu %>']
        # classification = [0, 0, 0, 0, 0, 2, 1, 1, 1]
        # mass = "<tonn>"
        # minerals = {'copper': ['%', '<Cu %>'], 'gold': ['oz/ton', '<Au (oz/ton)>'], 'silver': ['ppm', '<Ag [ppm]>']}
        # block_1 = Block(columns, mass, minerals, [0, 0, 0, 0, 5300, 1, 0.1, 0.0009999999999999998, 10.0],
        #                 classification)
        # block_2 = Block(columns, mass, minerals, [2, 0, 0, 2, 1700, 1, 0.1, 0.001, 10.0], classification)
        # block_3 = Block(columns, mass, minerals, [8, 0, 2, 0, 4400, 1, 0.1, 0.001, 10.0], classification)
        # block_4 = Block(columns, mass, minerals, [10, 0, 2, 2, 6200, 2, 0.1, 0.0009999999999999998, 10.0],
        #                 classification)

        block_model_1 = CreateBlockModel("test_model_file.csv")
        block_model_2 = CreateBlockModel("test_model_file.csv")
        self.assertEqual(block_model_2.__eq__(block_model_1), True)

    def test_print_mass_in_kilograms_when_block_exist_return_value_in_kilograms(self):
        columns = ['<id>', '<x>', '<y>', '<z>', '<tonn>', '<destination>', '<Au (oz/ton)>', '<Ag [ppm]>', '<Cu %>']
        classification = [0, 0, 0, 0, 0, 2, 1, 1, 1]
        mass = "<tonn>"
        minerals = {'copper': ['%', '<Cu %>'], 'gold': ['oz/ton', '<Au (oz/ton)>'], 'silver': ['ppm', '<Ag [ppm]>']}
        block_1 = Block(columns, mass, minerals, [0, 0, 0, 0, 5300, 1, 0.1, 0.0009999999999999998, 10.0],
                        classification)
        block_2 = Block(columns, mass, minerals, [2, 0, 0, 2, 1700, 1, 0.1, 0.001, 10.0], classification)
        block_3 = Block(columns, mass, minerals, [8, 0, 2, 0, 4400, 1, 0.1, 0.001, 10.0], classification)
        block_4 = Block(columns, mass, minerals, [10, 0, 2, 2, 6200, 2, 0.1, 0.0009999999999999998, 10.0],
                        classification)
        block_map = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        block_map['0']['0']['0'] = block_1
        block_map['0']['0']['2'] = block_2
        block_map['0']['2']['0'] = block_3
        block_map['0']['2']['2'] = block_4
        block_model_1 = BlockModel(columns, [block_1, block_2, block_3, block_4], block_map)
        self.assertEqual(printMassInKilograms(block_model_1, 0, 0, 0), str(float("5300.0")*1000)+"kg")

    def test_print_mass_in_kilograms_when_block_does_not_exist_return_message(self):
        columns = ['<id>', '<x>', '<y>', '<z>', '<tonn>', '<destination>', '<Au (oz/ton)>', '<Ag [ppm]>', '<Cu %>']
        classification = [0, 0, 0, 0, 0, 2, 1, 1, 1]
        mass = "<tonn>"
        minerals = {'copper': ['%', '<Cu %>'], 'gold': ['oz/ton', '<Au (oz/ton)>'], 'silver': ['ppm', '<Ag [ppm]>']}

        block_1 = Block(columns, mass, minerals, [0, 0, 0, 0, 5300, 1, 0.1, 0.0009999999999999998, 10.0],
                        classification)
        block_2 = Block(columns, mass, minerals, [2, 0, 0, 2, 1700, 1, 0.1, 0.001, 10.0], classification)
        block_3 = Block(columns, mass, minerals, [8, 0, 2, 0, 4400, 1, 0.1, 0.001, 10.0], classification)
        block_4 = Block(columns, mass, minerals, [10, 0, 2, 2, 6200, 2, 0.1, 0.0009999999999999998, 10.0],
                        classification)

        block_map = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        block_model_1 = BlockModel(columns, [block_1, block_2, block_3, block_4], block_map)
        self.assertEqual(printMassInKilograms(block_model_1, 0, 5, 20), "Block does not exist")

    def test_load_block_model_when_file_created_return_a_1(self):
        self.assertEqual(LoadBlockModel("test_model_file.csv", "test_output.csv"), 1)

    def test_extract_when_block_exists_return_array(self):
        columns = ['id', 'x', 'y', 'z', 'tonn', 'destination', 'Au (oz/ton)', 'Ag [ppm]', 'Cu %']
        classification = [0, 0, 0, 0, 0, 2, 1, 1, 1]
        mass = "tonn"
        minerals = {'copper': ['%', 'Cu %'], 'gold': ['oz/ton', 'Au (oz/ton)'], 'silver': ['ppm', 'Ag [ppm>']}
        block_1 = Block(columns, mass, minerals, [0, 0, 0, 0, 5300, 1, 0.1, 0.0009999999999999998, 10.0],
                        classification)
        block_2 = Block(columns, mass, minerals, [2, 0, 0, 2, 1700, 1, 0.1, 0.001, 10.0], classification)
        block_3 = Block(columns, mass, minerals, [8, 0, 2, 0, 4400, 1, 0.1, 0.001, 10.0], classification)
        block_4 = Block(columns, mass, minerals, [10, 0, 2, 2, 6200, 2, 0.1, 0.0009999999999999998, 10.0],
                        classification)
        block_1.precedence.append(block_2)
        block_1.precedence.append(block_3)
        block_1.precedence.append(block_4)
        block_2.precedence.append(block_3)
        block_3.precedence.append(block_4)

        expected = [{"index": '0'}, {"index": '2'}, {"index": '8'}, {"index": '10'}]

        self.assertEquals(extract(block_1), expected)

    def test_extract_when_block_does_not_exist_return_empty_array(self):
        self.assertEquals(extract(None), [])

    def test_extract_when_precedence_is_empty(self):
        columns = ['id', 'x', 'y', 'z', 'tonn', 'destination', 'Au (oz/ton)', 'Ag [ppm]', 'Cu %']
        classification = [0, 0, 0, 0, 0, 2, 1, 1, 1]
        mass = "tonn"
        minerals = {'copper': ['%', 'Cu %'], 'gold': ['oz/ton', 'Au (oz/ton)'], 'silver': ['ppm', 'Ag [ppm>']}
        block_1 = Block(columns, mass, minerals, [0, 0, 0, 0, 5300, 1, 0.1, 0.0009999999999999998, 10.0],
                        classification)

        expected = [{"index": '0'}]

        self.assertEquals(extract(block_1), expected)

    def test_extract_when_precedence_is_linear(self):
        
        columns = ['id', 'x', 'y', 'z', 'tonn', 'destination', 'Au (oz/ton)', 'Ag [ppm]', 'Cu %']
        classification = [0, 0, 0, 0, 0, 2, 1, 1, 1]
        mass = "tonn"
        minerals = {'copper': ['%', 'Cu %'], 'gold': ['oz/ton', 'Au (oz/ton)'], 'silver': ['ppm', 'Ag [ppm>']}
        block_1 = Block(columns, mass, minerals, [0, 0, 0, 0, 5300, 1, 0.1, 0.0009999999999999998, 10.0],
                        classification)
        block_2 = Block(columns, mass, minerals, [2, 0, 0, 2, 1700, 1, 0.1, 0.001, 10.0], classification)
        block_3 = Block(columns, mass, minerals, [8, 0, 2, 0, 4400, 1, 0.1, 0.001, 10.0], classification)
        block_4 = Block(columns, mass, minerals, [10, 0, 2, 2, 6200, 2, 0.1, 0.0009999999999999998, 10.0],
                        classification)
        block_1.precedence.append(block_2)
        block_2.precedence.append(block_3)
        block_3.precedence.append(block_4)

        expected = [{"index": '0'}, {"index": '2'}, {"index": '8'}, {"index": '10'}]

        self.assertEquals(extract(block_1), expected)

if __name__ == '__main__':
    unittest.main()