import hashlib
import os

class Hasher:
    def __init__(self, db=None):
        self.db = db
    
    def calculate_hash(self, file_path: str) -> str:
        if self.db:
            cached = self.db.get_hash(file_path)
            if cached:
                return cached
        
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        
        hash_value = hash_sha256.hexdigest()
        
        if self.db:
            self.db.save(file_path, hash_value)
        
        return hash_value