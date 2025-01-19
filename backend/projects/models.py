from django.db import models
import hashlib
import json
from jsonfield import JSONField
import base64
import numpy as np

# Create your models here.
class Gallery(models.Model):
    image = models.ImageField(null=True, blank=True)


class ImageAddress(models.Model):
    image = models.ImageField(upload_to='images/')
    address = models.CharField(max_length=100)


class Block(models.Model):
    index = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)
    column_hash = models.TextField()
    encrypted_Y = JSONField(null=True, blank=True)
    encrypted_Cb = JSONField(null=True, blank=True)
    encrypted_Cr = JSONField(null=True, blank=True)

    def __str__(self):
        return f"Block {self.index}"

    def save(self, *args, **kwargs):
        # Encode binary data before saving
        if isinstance(self.encrypted_Y, bytes):
            self.encrypted_Y = base64.b64encode(self.encrypted_Y).decode('utf-8')
        if isinstance(self.encrypted_Cb, bytes):
            self.encrypted_Cb = base64.b64encode(self.encrypted_Cb).decode('utf-8')
        if isinstance(self.encrypted_Cr, bytes):
            self.encrypted_Cr = base64.b64encode(self.encrypted_Cr).decode('utf-8')

        # Calculate the hash and save the block
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

    def calculate_hash(self):
        # Create the block string for hashing
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "column_hash": self.column_hash,
            "previous_hash": self.previous_hash,
            "encrypted_Y": self.encrypted_Y,
            "encrypted_Cb": self.encrypted_Cb,
            "encrypted_Cr": self.encrypted_Cr,
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def get_decrypted_data(self):
        # Decode base64-encoded data back to bytes
        decrypted_data = {}
        if self.encrypted_Y:
            decrypted_data['Y'] = base64.b64decode(self.encrypted_Y.encode('utf-8'))
        if self.encrypted_Cb:
            decrypted_data['Cb'] = base64.b64decode(self.encrypted_Cb.encode('utf-8'))
        if self.encrypted_Cr:
            decrypted_data['Cr'] = base64.b64decode(self.encrypted_Cr.encode('utf-8'))
        return decrypted_data

    
    @classmethod
    def create_genesis_block(cls, encrypted_data=None):
        if not cls.objects.exists():
            genesis_block = cls.objects.create(
                index=0,
                previous_hash="0",
                hash="0",  # You may need to adjust this depending on your hashing logic
                encrypted_Y=encrypted_data,  # Save encrypted data
                encrypted_Cb=encrypted_data,
                encrypted_Cr=encrypted_data,
            )
            return genesis_block

    @classmethod
    def get_block_by_index(cls, index):
        try:
            return cls.objects.get(index=index)
        except Block.DoesNotExist:
            return None
