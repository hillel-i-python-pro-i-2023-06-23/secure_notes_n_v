from django.db import models
from cryptography.fernet import Fernet

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    key = models.BinaryField()
    encrypted_content = models.BinaryField()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = Fernet.generate_key()
        cipher_suite = Fernet(self.key)
        encrypted_content = cipher_suite.encrypt(self.content.encode('utf-8'))
        self.encrypted_content = encrypted_content
        super(Note, self).save(*args, **kwargs)

    def decrypt_content(self):
        cipher_suite = Fernet(self.key)
        decrypted_content = cipher_suite.decrypt(self.encrypted_content).decode('utf-8')
        return decrypted_content
