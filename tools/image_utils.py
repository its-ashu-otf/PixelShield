import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from typing import Tuple

SUPPORTED_FORMATS = {
    'JPEG': ['.jpg', '.jpeg', '.jpe', '.jfif'],
    'PNG': ['.png'],
    'BMP': ['.bmp', '.dib'],
    'GIF': ['.gif'],
    'TIFF': ['.tiff', '.tif'],
    'WebP': ['.webp'],
    'ICO': ['.ico'],
    'HEIC': ['.heic', '.heif'],
    'AVIF': ['.avif'],
    'SVG': ['.svg'],
    'RAW': ['.raw', '.cr2', '.nef', '.arw', '.dng'],
    'PBM': ['.pbm'],
    'PGM': ['.pgm'],
    'PPM': ['.ppm'],
    'XBM': ['.xbm'],
    'XPM': ['.xpm'],
}

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from the password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_image(input_path: str, output_path: str, password: str):
    """Encrypt an image using AES-GCM."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file '{input_path}' does not exist.")

    salt = os.urandom(16)  # Generate a random salt
    key = derive_key(password, salt)  # Derive encryption key

    iv = os.urandom(12)  # AES-GCM standard IV size
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag  # Authentication tag (important for GCM mode)

    # Store (Salt + IV + Tag + Ciphertext)
    with open(output_path, 'wb') as f:
        f.write(salt + iv + tag + ciphertext)

def decrypt_image(input_path: str, output_path: str, password: str):
    """Decrypt an image encrypted with AES-GCM."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file '{input_path}' does not exist.")

    with open(input_path, 'rb') as f:
        encrypted_data = f.read()

    # Ensure the file is large enough to contain Salt, IV, Tag, and Ciphertext
    if len(encrypted_data) < 44:
        raise ValueError("Invalid encrypted file format.")

    # Extract Salt, IV, Tag, and Ciphertext
    salt = encrypted_data[:16]
    iv = encrypted_data[16:28]
    tag = encrypted_data[28:44]
    ciphertext = encrypted_data[44:]

    key = derive_key(password, salt)  # Derive decryption key

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        with open(output_path, 'wb') as f:
            f.write(plaintext)
    except Exception as e:
        raise ValueError("Decryption failed. Incorrect password or corrupted file.") from e

def is_supported_image(file_path: str) -> Tuple[bool, str]:
    """Check if the file is a supported image format."""
    ext = os.path.splitext(file_path)[1].lower()
    supported_extensions = [ext for formats in SUPPORTED_FORMATS.values() for ext in formats]
    
    if ext not in supported_extensions:
        return False, f"Unsupported file format '{ext}'. Supported formats: {', '.join(supported_extensions)}"
    
    return True, ""