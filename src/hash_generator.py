"""
A module that generates a hash value for a given input string.
"""
import hashlib


class HashGenerator: # pylint: disable=R0903
    """
    A class that generates a hash value for a given input string.

    Attributes:
        hash_length (int): The length of the generated hash value.

    Methods:
        generate(input: str, salt: str = "") -> str:
            Generates a hash value for the given input string with an optional salt.
        _hash_string(input: str) -> str:
            Hashes the input string using the SHA-256 algorithm and returns the hash value.
    """

    hash_length = 5

    def generate(self, input_string: str, salt: str = "") -> str:
        """
        Generates a hash value for the given input string with an optional salt.

        Args:
            input (str): The input string to be hashed.
            salt (str, optional): An optional salt string to be appended to the input string
            before hashing.

        Returns:
            str: The generated hash value.
        """
        hash_input = f"{input_string}{salt}"
        return self._hash_string(hash_input)

    def _hash_string(self, input_string: str) -> str:
        """
        Hashes the input string using the SHA-256 algorithm and returns the hash value.

        Args:
            input (str): The input string to be hashed.

        Returns:
            str: The hash value of the input string.
        """
        return hashlib.sha256(input_string.encode()).hexdigest()[: self.hash_length]
