import ctypes
import platform
import tkinter as tk
from tkinter import font

def setup_dpi_awareness():
    """Set up DPI awareness for the application."""
    if platform.system() == 'Windows':
        try:
            # Set per-monitor DPI awareness
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            # Fallback to system-wide DPI awareness
            ctypes.windll.shcore.SetProcessDpiAwareness(2)

def setup_scaling(root: tk.Tk):
    """Configure Tkinter scaling and fonts."""
    # Get screen DPI
    dpi = root.winfo_fpixels('1i')
    scale_factor = dpi / 96.0  # 96 DPI is the standard
    
    # Set Tk scaling
    root.tk.call('tk', 'scaling', scale_factor)
    
    # Create default fonts with appropriate sizes
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=int(10 * scale_factor))
    
    # Configure other common fonts
    text_font = font.Font(size=int(12 * scale_factor))
    heading_font = font.Font(size=int(14 * scale_factor), weight="bold")
    
    return {
        'default': default_font,
        'text': text_font,
        'heading': heading_font,
        'scale_factor': scale_factor
    }

def get_scaled_size(base_size: int, scale_factor: float) -> int:
    """Calculate scaled size based on DPI scale factor."""
    return int(base_size * scale_factor)

def create_scaled_frame(parent: tk.Widget, scale_factor: float) -> tk.Frame:
    """Create a frame with proper scaling configuration."""
    frame = tk.Frame(parent)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    return frame 