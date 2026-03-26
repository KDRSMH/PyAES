import base64
import binascii
import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def derive_aes_key(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()


def encrypt_text(plaintext: str, password: str) -> str:
    key = derive_aes_key(password)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = pad(plaintext.encode("utf-8"), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return base64.b64encode(iv + ciphertext).decode("utf-8")


def decrypt_text(encrypted_b64: str, password: str) -> str:
    key = derive_aes_key(password)
    try:
        encrypted_data = base64.b64decode(encrypted_b64)
        if len(encrypted_data) <= 16:
            raise ValueError("Geçersiz veri uzunluğu")

        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, AES.block_size)
        return plaintext.decode("utf-8")
    except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
        raise ValueError("Hatalı Parola veya Bozuk Veri!") from exc
