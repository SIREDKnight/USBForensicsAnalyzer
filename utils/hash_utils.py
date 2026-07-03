import hashlib
import json


class HashUtils:

    @staticmethod
    def sha256(data):

        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)

        return hashlib.sha256(str(data).encode()).hexdigest()