#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from tools.image_utils import encrypt_image, decrypt_image, is_supported_image, SUPPORTED_FORMATS
from gui.main_window import PixelShieldApp as PixelShieldGUI  # Import the GUI application

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent))

# ANSI color codes for CLI output
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
{GREEN}                ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═════╝{END}
{CYAN}                                     Secure Image Encryption Tool                                {END}
{CYAN}                                        Version 1.0.0 - 2025                                     {END}
""")


def handle_encrypt(args):
    """Handle the encryption command."""
    valid, error_msg = is_supported_image(args.input)
    if not valid:
        print(f"{RED}Error: {error_msg}{END}")
        return

    try:
        encrypt_image(args.input, args.output, args.key)
        print(f"{GREEN}Image encrypted successfully: {args.output}{END}")
    except Exception as e:
        print(f"{RED}Encryption failed: {e}{END}")


def handle_decrypt(args):
    """Handle the decryption command."""
    try:
        decrypt_image(args.input, args.output, args.key)
        print(f"{GREEN}Image decrypted successfully: {args.output}{END}")
    except Exception as e:
        print(f"{RED}Decryption failed: {e}{END}")


def handle_formats():
    """Handle the formats command."""
    print(f"\n{CYAN}Supported Image Formats:{END}")
    for format_name, extensions in SUPPORTED_FORMATS.items():
        print(f"{YELLOW}{format_name}:{END} {', '.join(extensions)}")


def parse_arguments():
    """Parse command-line arguments."""
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
"""
    )

    parser.add_argument('-gui', '--gui', action='store_true', help='Launch the graphical user interface')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Encrypt command
    encrypt_parser = subparsers.add_parser(
        'encrypt',
        help='Encrypt an image file',
        description='Encrypt an image file using AES-256 encryption'
    )
    encrypt_parser.add_argument('--input', required=True, help='Path to input image file')
    encrypt_parser.add_argument('--output', required=True, help='Path to save encrypted output file')
    encrypt_parser.add_argument('--key', required=True, help='Encryption password/key')

    # Decrypt command
    decrypt_parser = subparsers.add_parser(
        'decrypt',
        help='Decrypt an encrypted image file',
        description='Decrypt a previously encrypted image file'
    )
    decrypt_parser.add_argument('--input', required=True, help='Path to encrypted input file')
    decrypt_parser.add_argument('--output', required=True, help='Path to save decrypted image')
    decrypt_parser.add_argument('--key', required=True, help='Decryption password/key (must match encryption password)')

    # List formats command
    subparsers.add_parser(
        'formats',
        help='List all supported image formats',
        description='Display a list of all image formats supported by PixelShield'
    )

    return parser.parse_args()


def main():
    """Main entry point for the application."""
    print_banner()
    args = parse_arguments()

    if args.gui:
        app = PixelShieldGUI()
        app.mainloop()
        return

    if args.command == 'encrypt':
        handle_encrypt(args)
    elif args.command == 'decrypt':
        handle_decrypt(args)
    elif args.command == 'formats':
        handle_formats()
    else:
        print("Invalid command. Use --help for usage information.")


if __name__ == '__main__':
    main()