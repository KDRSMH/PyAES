# PyAES
A GUI-based cryptography tool implementing AES-256 (CBC mode) with SHA-256 key hashing. Developed using PyQt and PyCryptodome.

## Kurulum

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Çalıştırma

```bash
python3 main.py
```

## Özellikler

- AES-256 (CBC) şifreleme ve şifre çözme
- SHA-256 ile parola tabanlı 32 byte anahtar üretimi
- Rastgele 16 byte IV kullanımı
- PKCS7 padding / unpadding
- Base64 çıktı biçimi
