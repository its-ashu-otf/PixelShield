# PixelShield - Image Encryption Tool

PixelShield is a powerful image encryption tool that secures your image files using strong encryption algorithms. It protects your visual data from unauthorized access and tampering.

## Features

- Secure image encryption using AES-256 encryption
- Support for 15+ image formats including:
  - Common formats: JPEG, PNG, BMP, GIF, TIFF, WebP, ICO
  - Modern formats: HEIC, AVIF, SVG
  - Raw formats: RAW, CR2, NEF, ARW, DNG
  - Other formats: PBM, PGM, PPM, XBM, XPM
- Simple command-line interface with colorful output
- User-friendly graphical interface
- Preserves image metadata
- Secure key generation and management
- Comprehensive error handling and validation
- File integrity verification

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

#### Basic Commands

1. **Encrypt an Image**:
```bash
python pixel_shield.py encrypt --input image.jpg --output encrypted.bin --key "your_password"
```

2. **Decrypt an Image**:
```bash
python pixel_shield.py decrypt --input encrypted.bin --output decrypted.jpg --key "your_password"
```

3. **List Supported Formats**:
```bash
python pixel_shield.py formats
```

#### Examples

- Encrypt a PNG image:
```bash
python pixel_shield.py encrypt --input photo.png --output secure.enc --key "mysecret"
```

- Decrypt a RAW image:
```bash
python pixel_shield.py decrypt --input secure.enc --output photo.raw --key "mysecret"
```

### Graphical Interface

To launch the graphical interface:
```bash
python pixel_shield_gui.py
```

The GUI provides:
- File selection dialogs with format filtering
- Password input field with secure masking
- Encrypt/Decrypt buttons
- Status indicators
- Error messages and success notifications
- Automatic output filename suggestion

## Security Features

- Uses AES-256 encryption (industry standard)
- Implements secure key derivation using PBKDF2
- Adds salt to prevent rainbow table attacks
- Includes integrity verification
- Preserves original image format
- Secure password handling
- File validation and corruption detection

## Error Handling

The tool provides detailed error messages for various scenarios:
- Unsupported file formats
- Missing or empty files
- Corrupted images
- Invalid passwords
- Encryption/decryption failures
- File access issues

## Requirements

- Python 3.8 or higher
- Dependencies listed in requirements.txt
- tkinter (usually comes with Python)
- PIL (Pillow) for image processing
- cryptography for encryption

## Supported Image Formats

The tool supports a wide range of image formats:

### Common Formats
- JPEG (.jpg, .jpeg, .jpe, .jfif)
- PNG (.png)
- BMP (.bmp, .dib)
- GIF (.gif)
- TIFF (.tiff, .tif)
- WebP (.webp)
- ICO (.ico)

### Modern Formats
- HEIC (.heic, .heif)
- AVIF (.avif)
- SVG (.svg)

### Raw Formats
- RAW (.raw, .cr2, .nef, .arw, .dng)

### Other Formats
- PBM (.pbm)
- PGM (.pgm)
- PPM (.ppm)
- XBM (.xbm)
- XPM (.xpm)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Version History

- v0.1.2 (2025)
  - Added support for 15+ image formats
  - Enhanced error handling
  - Improved GUI interface
  - Added colorful CLI output
  - Added file validation 