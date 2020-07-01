import unittest
from main import *
import json

class TestReblockFunctions(unittest.TestCase):
    def test_block_models_when_response_is_false_returns_string_json(self):
        self.assertIsInstance(block_models(), str)

    def test_reblock_model_when_test_data_used_and_x_y_z_equals_0_returns_status_ok(self):
        result = status_code = {status.HTTP_200_OK:  'OK'}
        self.assertEqual(reblock_model('test_data', 1, 1, 1), result)

if __name__ == '__main__':
    unittest.main()