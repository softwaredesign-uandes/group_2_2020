import unittest
from main import *
import json

class TestReblockFunctions(unittest.TestCase):
    def test_block_models_when_response_is_false_returns_string_json(self):
        self.assertIsInstance(block_models(), str)

    def test_loaded_blocks_when_response_is_false_returns_list_string(self):
        data = json.dumps([{"index": "0", "x": "0", "y": "0", "z": "0", "tonn": "5300", "destination": "1", "Au (oz/ton)": "0.1", "Ag [ppm]": "0.0009999999999999998", "Cu %": "10.0"}, {"index": "2", "x": "0", "y": "0", "z": "2", "tonn": "1700", "destination": "1", "Au (oz/ton)": "0.1", "Ag [ppm]": "0.001", "Cu %": "10.0"}, {"index": "8", 
                            "x": "0", "y": "2", "z": "0", "tonn": "4400", "destination": "1", "Au (oz/ton)": "0.1", "Ag [ppm]": "0.001", "Cu %": "10.0"}, {"index": "10", "x": "0", "y": "2", "z": "2", "tonn": "6200", "destination": "2", "Au (oz/ton)": "0.1", "Ag [ppm]": "0.0009999999999999998", "Cu %": "10.0"}, {"index": "32", "x": "2", "y": "0", "z": "0", "tonn": "4400", "destination": "1", "Au (oz/ton)": "0.1", "Ag [ppm]": "0.0009999999999999998", "Cu %": "10.0"}, {"index": "34", "x": "2", "y": "0", "z": "2", "tonn": "4400", "destination": "2", "Au (oz/ton)": "0.1", "Ag [ppm]": "0.001", "Cu %": "10.0"}, {"index": "40", "x": "2", "y": "2", "z": "0", "tonn": "2600", "destination": "2", "Au (oz/ton)": "0.1", "Ag [ppm]": "0.001", "Cu %": "10.0"}, {"index": "42", "x": "2", "y": "2", "z": "2", "tonn": "2600", "destination": "1", "Au (oz/ton)": "0.1", "Ag [ppm]": "0.001", "Cu %": "10.0"}])
        self.assertEqual(loaded_blocks('test_data_reblocked'), data)

    def test_index_block_when_response_is_false_returns_None(self):
        self.assertEqual(index_block('test_data_reblocked', 0), None)

    def test_reblock_model_when_test_data_used_and_x_y_z_equals_0_returns_status_ok(self):
        result = status_code = {status.HTTP_200_OK:  'OK'}
        self.assertEqual(reblock_model('test_data', 1, 1, 1), result)