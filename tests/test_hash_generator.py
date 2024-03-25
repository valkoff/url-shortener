import unittest
from src.hash_generator import HashGenerator


class TestHashGenerator(unittest.TestCase):
    def setUp(self):
        self.hash_generator = HashGenerator()

    def test_can_generate_hash(self):
        input_string = "example"
        salt = "abc"
        expected_hash = "57cbf"

        generated_hash = self.hash_generator.generate(input_string, salt)

        self.assertEqual(generated_hash, expected_hash)

    def test_can_generate_hash_without_salt(self):
        input_string = "example"
        expected_hash = "50d85"

        generated_hash = self.hash_generator.generate(input_string)

        self.assertEqual(generated_hash, expected_hash)

    def test_can_generate_different_hashes_for_different_inputs(self):
        input_string_1 = "example1"
        input_string_2 = "example2"

        generated_hash_1 = self.hash_generator.generate(input_string_1)
        generated_hash_2 = self.hash_generator.generate(input_string_2)

        self.assertNotEqual(generated_hash_1, generated_hash_2)
