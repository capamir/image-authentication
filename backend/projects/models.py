from django.db import models

import hashlib
import json
from jsonfield import JSONField
# Create your models here.
class Gallery(models.Model):
    image = models.ImageField(null=True, blank=True)


class ImageAddress(models.Model):
    image = models.ImageField(upload_to='images/')
    address = models.CharField(max_length=100)


models.ImageField(null=True, blank=True)
class Block(models.Model):
    index = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)
    encrypted_data = JSONField(null=True, blank=True)
    
    
          # New field for encrypted data

    def __str__(self):
        return f"Block {self.index}"
    

    def save_encrypted_data(self, encrypted_data):
   
        # Implement your serialization logic here
        serialized_data = self.serialize_encrypted_data(encrypted_data)
        self.encrypted_data = serialized_data
        self.save()

    def serialize_encrypted_data(self, encrypted_data):

        serialized_data = {}  # You can customize this based on your data structure
        for key, value in encrypted_data.items():
            serialized_data[key] = (
                value[0].hex(),  # Convert bytes to hexadecimal string for storage
                value[1].hex()
            )
        return serialized_data

    def deserialize_encrypted_data(self):
       
        decrypted_data = {}
        for key, value in self.encrypted_data.items():
            decrypted_data[key] = (
                bytes.fromhex(value[0]),  # Convert hexadecimal string back to bytes
                bytes.fromhex(value[1])
            )
        return decrypted_data

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "encrypted_data": self.encrypted_data,  # Include encrypted data in the hash calculation
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def save(self, *args, **kwargs):
        if not self.pk:  # If the block is being created (not updated)
            if not Block.objects.exists():  # If there are no blocks in the database
                self.index = 0
                self.previous_hash = "0"
                self.hash = "0"  # You may need to adjust this depending on your hashing logic
            else:
                try:
                    previous_block = Block.objects.latest('index')
                    self.index = previous_block.index + 1
                    self.previous_hash = previous_block.hash
                except Block.DoesNotExist:
                    raise ValueError("Previous block does not exist.")
            self.hash = self.calculate_hash()
        super().save(*args, **kwargs)

    @classmethod
    def create_genesis_block(cls, encrypted_data=None):
        if not cls.objects.exists():
            genesis_block = cls.objects.create(
                index=0,
                data="Genesis Block",
                previous_hash="0",
                hash="0",  # You may need to adjust this depending on your hashing logic
                encrypted_data=encrypted_data  # Save encrypted data
            )
            return genesis_block
    

    @classmethod
    def get_block_by_index(cls, index):
        try:
            return cls.objects.get(index=index)
        except Block.DoesNotExist:
            return None
