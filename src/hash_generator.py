import hashlib


class HashGenerator:
    hash_length = 5

    def generate(self, input: str, salt: str = "") -> str:
        hash_input = f"{input}{salt}"
        return self._hash_string(hash_input)

    def _hash_string(self, input: str) -> str:
        return hashlib.sha256(input.encode()).hexdigest()[: self.hash_length]
