#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent))

from tools.image_utils import encrypt_image, decrypt_image, is_supported_image

# ANSI color codes
BOLD = '\033[1m'
END = '\033[0m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'

def print_banner():
    """Print a colorful banner for the application."""
    print(f"""
{GREEN}                ██████╗ ██╗██╗  ██╗███████╗██╗     ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ {END}
{GREEN}                ██╔══██╗██║╚██╗██╔╝██╔════╝██║     ██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗{END}
{GREEN}                ██████╔╝██║ ╚███╔╝ █████╗  ██║     ███████╗███████║██║█████╗  ██║     ██║  ██║{END}
{GREEN}                ██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║     ╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║{END}
{GREEN}                ██║     ██║██╔╝ ██╗███████╗███████╗███████║██║  ██║██║███████╗███████╗██████╔╝{END}
{GREEN}                ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝{END}
{CYAN}                                     Secure Image Encryption Tool                                {END}
{CYAN}                                        Version 0.2.0 - 2025                                     {END}
""")

def main():
    # Print banner for CLI mode
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

  Launch GUI:
    {GREEN}%(prog)s -gui{END}

{CYAN}Notes:{END}
  - Passwords should be strong and kept secure
  - Encrypted files will have .bin extension by default
  - Original image format is preserved after decryption
""")

    parser.add_argument('-gui', '--gui', action='store_true',
                       help='Launch the graphical user interface')
    
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
        valid, error_msg = is_supported_image(args.input)
        if not valid:
            print(f"{RED}Error: {error_msg}{END}")
            return
        
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