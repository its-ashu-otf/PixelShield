#!/usr/bin/env python3
import argparse
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PIL import Image
import base64
import numpy as np
import io
import mimetypes
from pathlib import Path

# ANSI color codes
BLUE = '\033[94m'
BOLD = '\033[1m'
END = '\033[0m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'

# Supported image formats
SUPPORTED_FORMATS = {
    # Common formats
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
    # Raw formats
    'RAW': ['.raw', '.cr2', '.nef', '.arw', '.dng'],
    # Other formats
    'PBM': ['.pbm'],
    'PGM': ['.pgm'],
    'PPM': ['.ppm'],
    'XBM': ['.xbm'],
    'XPM': ['.xpm']
}

def get_supported_extensions():
    """Get a list of all supported file extensions."""
    return [ext for formats in SUPPORTED_FORMATS.values() for ext in formats]

def is_supported_image(file_path: str) -> tuple[bool, str]:
    """
    Check if the file is a supported image format.
    Returns (is_supported, error_message)
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return False, f"{RED}Error: File '{file_path}' does not exist{END}"
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return False, f"{RED}Error: File '{file_path}' is empty{END}"
        
        # Check file extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in get_supported_extensions():
            return False, f"{RED}Error: Unsupported file format '{ext}'. Supported formats: {', '.join(get_supported_extensions())}{END}"
        
        # Try to open the image
        try:
            with Image.open(file_path) as img:
                # Verify it's a valid image
                img.verify()
                return True, ""
        except Exception as e:
            return False, f"{RED}Error: Invalid or corrupted image file: {str(e)}{END}"
            
    except Exception as e:
        return False, f"{RED}Error: Failed to process file: {str(e)}{END}"

def print_banner():
    """Print a colorful banner for the application."""
    # Define additional colors
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    
    # Randomly choose colors for different parts
    colors = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]
    import random
    title_color = random.choice(colors)
    subtitle_color = random.choice(colors)
    version_color = random.choice(colors)
    
    banner = f"""
{title_color}                ██████╗ ██╗██╗  ██╗███████╗██╗     ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ {END}
{title_color}                ██╔══██╗██║╚██╗██╔╝██╔════╝██║     ██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗{END}
{title_color}                ██████╔╝██║ ╚███╔╝ █████╗  ██║     ███████╗███████║██║█████╗  ██║     ██║  ██║{END}
{title_color}                ██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║     ╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║{END}
{title_color}                ██║     ██║██╔╝ ██╗███████╗███████╗███████║██║  ██║██║███████╗███████╗██████╔╝{END}
{title_color}                ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝{END}
{subtitle_color}                                     Secure Image Encryption Tool                                {END}
{version_color}                                        Version 0.2.0 - 2025                                     {END}
{version_color}                                Supporting {len(SUPPORTED_FORMATS)} Image Formats                                {END}
"""
    print(banner)

def derive_key(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """Derive a key from the password using PBKDF2."""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_image(input_path: str, output_path: str, password: str) -> None:
    """Encrypt an image file."""
    # Validate input file
    is_valid, error_msg = is_supported_image(input_path)
    if not is_valid:
        print(error_msg)
        return
    
    try:
        # Read the raw image data without any processing
        with open(input_path, 'rb') as f:
            image_data = f.read()
        
        # Generate key and salt
        key, salt = derive_key(password)
        
        # Create Fernet instance
        f = Fernet(key)
        
        # Encrypt the raw image data
        encrypted_data = f.encrypt(image_data)
        
        # Combine salt and encrypted data
        final_data = salt + encrypted_data
        
        # Save the encrypted data
        with open(output_path, 'wb') as f:
            f.write(final_data)
            
    except Exception as e:
        print(f"{RED}Error: Failed to encrypt image: {str(e)}{END}")
        return

def decrypt_image(input_path: str, output_path: str, password: str) -> None:
    """Decrypt an image file."""
    try:
        # Validate input file exists and is not empty
        if not os.path.exists(input_path):
            print(f"{RED}Error: Encrypted file '{input_path}' does not exist{END}")
            return
            
        if os.path.getsize(input_path) == 0:
            print(f"{RED}Error: Encrypted file '{input_path}' is empty{END}")
            return
        
        # Read the encrypted data
        with open(input_path, 'rb') as f:
            data = f.read()
        
        # Extract salt and encrypted data
        salt = data[:16]
        encrypted_data = data[16:]
        
        # Derive key using the same salt
        key, _ = derive_key(password, salt)
        
        # Create Fernet instance
        f = Fernet(key)
        
        try:
            # Decrypt the data
            decrypted_data = f.decrypt(encrypted_data)
            
            # Write the decrypted data directly to the output file
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)
                
        except Exception as e:
            print(f"{RED}Error: Failed to decrypt image. Make sure the password is correct: {str(e)}{END}")
            return
            
    except Exception as e:
        print(f"{RED}Error: Failed to process encrypted file: {str(e)}{END}")
        return

def main():
    # Print banner
    print_banner()
    
    parser = argparse.ArgumentParser(
        description=f'{BOLD}PixelShield - Secure Image Encryption Tool{END}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{CYAN}Examples:{END}
  Encrypt an image:
    {GREEN}%(prog)s encrypt --input image.jpg --output encrypted.bin --key "mysecretpassword"{END}
    
  Decrypt an image:
    {GREEN}%(prog)s decrypt --input encrypted.bin --output decrypted.jpg --key "mysecretpassword"{END}
    
  List supported formats:
    {GREEN}%(prog)s formats{END}

{CYAN}Notes:{END}
  - Passwords should be strong and kept secure
  - Encrypted files will have .bin extension by default
  - Original image format is preserved after decryption
""")

    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', 
        help='Encrypt an image file',
        description='Encrypt an image file using AES-256 encryption')
    encrypt_parser.add_argument('--input', required=True, help='Path to input image file')
    encrypt_parser.add_argument('--output', required=True, help='Path to save encrypted output file')
    encrypt_parser.add_argument('--key', required=True, help='Encryption password/key')
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt',
        help='Decrypt an encrypted image file', 
        description='Decrypt a previously encrypted image file')
    decrypt_parser.add_argument('--input', required=True, help='Path to encrypted input file')
    decrypt_parser.add_argument('--output', required=True, help='Path to save decrypted image')
    decrypt_parser.add_argument('--key', required=True, help='Decryption password/key (must match encryption password)')
    
    # List formats command
    formats_parser = subparsers.add_parser('formats',
        help='List all supported image formats',
        description='Display a list of all image formats supported by PixelShield')
    
    args = parser.parse_args()
    
    if args.command == 'encrypt':
        encrypt_image(args.input, args.output, args.key)
        print(f"{GREEN}Image encrypted successfully: {args.output}{END}")
    elif args.command == 'decrypt':
        decrypt_image(args.input, args.output, args.key)
        print(f"{GREEN}Image decrypted successfully: {args.output}{END}")
    elif args.command == 'formats':
        print(f"\n{CYAN}Supported Image Formats:{END}")
        for format_name, extensions in SUPPORTED_FORMATS.items():
            print(f"{YELLOW}{format_name}:{END} {', '.join(extensions)}")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()